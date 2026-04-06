"""Remplace un sort du main pour introduire une couleur d'identité cible."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.deck_mutation import DeckMutation
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult
from baobab_mtg_deckbuilder.mutation.mutation_support import (
    assert_constructed_nonbasic_cap,
    assert_pool_covers_name,
    build_mutation_result,
    counts_map,
    map_to_sorted_entries,
    with_replaced_section,
)
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition


class ColorFixOperator(DeckMutationOperator):
    """Introduit ``target_color`` (WUBRG) en remplaçant un sort non-terrain du main."""

    def __init__(self, target_color: str) -> None:
        symbol = target_color.strip().upper()
        if symbol not in {"W", "U", "B", "R", "G"}:
            raise DeckMutationException(
                f"Couleur cible invalide pour ColorFixOperator : {target_color!r} "
                "(attendu : W, U, B, R ou G)."
            )
        self._target_color = symbol

    @property
    def operator_id(self) -> str:
        return "color_fix"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        if context.analytic_provider is None:
            raise DeckMutationException(
                "ColorFixOperator requiert un ``analytic_provider`` dans le contexte."
            )
        deck_before = context.deck
        main_counts = dict(counts_map(deck_before.main_section.entries))
        colors_present = _collect_main_identity_colors(main_counts, context.analytic_provider)
        if self._target_color in colors_present:
            raise DeckMutationException(
                f"La couleur {self._target_color} est déjà présente dans l'identité du main."
            )
        removable = _sorted_removable_nonlands(main_counts, context.analytic_provider)
        if not removable:
            raise DeckMutationException(
                "Aucun sort non-terrain du main ne peut être retiré pour corriger la couleur."
            )
        chosen = _search_color_fix_pair(
            deck_before=deck_before,
            main_counts=main_counts,
            removable=removable,
            pool=context.pool,
            target_color=self._target_color,
            provider=context.analytic_provider,
            format_definition=context.format_definition,
        )
        if chosen is None:
            raise DeckMutationException(
                f"Aucune carte du pool ne permet d'introduire proprement la couleur "
                f"{self._target_color}."
            )
        chosen_remove, chosen_add, deck_after = chosen
        mutation = DeckMutation(
            mutation_code="color_fix",
            message=(
                f"Remplacement de « {chosen_remove} » par « {chosen_add} » pour intégrer "
                f"la couleur {self._target_color}."
            ),
            section_identifier="main",
        )
        justification = (
            f"Ajout de la couleur d'identité {self._target_color} via un sort du pool "
            f"({chosen_remove} → {chosen_add})."
        )
        return build_mutation_result(
            operator_id=self.operator_id,
            deck_before=deck_before,
            deck_after=deck_after,
            mutations_applied=(mutation,),
            justification=justification,
            format_definition=context.format_definition,
            score_fn=context.score_fn,
        )


def _collect_main_identity_colors(
    main_counts: dict[str, int],
    provider: CardAnalyticProviderProtocol,
) -> set[str]:
    colors: set[str] = set()
    for name, qty in main_counts.items():
        if qty < 1:
            continue
        profile = provider.analytic_profile_for(name)
        if profile is None:
            continue
        colors |= set(profile.color_identity)
    return colors


def _sorted_removable_nonlands(
    main_counts: dict[str, int],
    provider: CardAnalyticProviderProtocol,
) -> list[str]:
    return sorted(
        (
            name
            for name, qty in main_counts.items()
            if qty >= 1 and _is_nonland_spell(provider, name)
        ),
        key=lambda n: (n.lower(), n),
    )


def _search_color_fix_pair(
    *,
    deck_before: Deck,
    main_counts: dict[str, int],
    removable: list[str],
    pool: CardPool,
    target_color: str,
    provider: CardAnalyticProviderProtocol,
    format_definition: FormatDefinition,
) -> tuple[str, str, Deck] | None:
    pool_candidates = sorted(
        (entry.english_oracle_name for entry in pool.entries),
        key=lambda n: (n.lower(), n),
    )
    for remove_name in removable:
        found = _try_remove_with_pool_add(
            deck_before=deck_before,
            main_counts=main_counts,
            remove_name=remove_name,
            pool_candidates=pool_candidates,
            target_color=target_color,
            provider=provider,
            pool=pool,
            format_definition=format_definition,
        )
        if found is not None:
            return found
    return None


def _try_remove_with_pool_add(
    *,
    deck_before: Deck,
    main_counts: dict[str, int],
    remove_name: str,
    pool_candidates: list[str],
    target_color: str,
    provider: CardAnalyticProviderProtocol,
    pool: CardPool,
    format_definition: FormatDefinition,
) -> tuple[str, str, Deck] | None:
    for add_name in pool_candidates:
        if add_name == remove_name:
            continue
        if not _is_nonland_spell(provider, add_name):
            continue
        profile = provider.analytic_profile_for(add_name)
        if profile is None or target_color not in profile.color_identity:
            continue
        trial_counts = dict(main_counts)
        trial_counts[remove_name] -= 1
        if trial_counts[remove_name] == 0:
            del trial_counts[remove_name]
        trial_counts[add_name] = trial_counts.get(add_name, 0) + 1
        trial_deck = with_replaced_section(
            deck_before,
            "main",
            map_to_sorted_entries(trial_counts),
        )
        try:
            assert_pool_covers_name(trial_deck, pool, add_name)
            assert_constructed_nonbasic_cap(trial_deck, format_definition)
        except DeckMutationException:
            continue
        return remove_name, add_name, trial_deck
    return None


def _is_nonland_spell(provider: CardAnalyticProviderProtocol, english_name: str) -> bool:
    """Vrai si le profil indique explicitement un non-terrain."""
    prof = provider.analytic_profile_for(english_name)
    return prof is not None and prof.is_land is False
