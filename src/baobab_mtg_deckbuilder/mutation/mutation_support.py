"""Fonctions utilitaires internes pour construire et valider les mutations."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping
from typing import Literal, TypeAlias

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.generation.maindeck_from_pool_builder import main_minimum_for_format
from baobab_mtg_deckbuilder.mutation.deck_mutation import DeckMutation
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult, MutationImpact
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition

SectionChoice: TypeAlias = Literal["main", "sideboard"]


def section_entries(deck: Deck, section: SectionChoice) -> tuple[DeckCardEntry, ...]:
    """Entrées de la section demandée."""
    if section == "main":
        return deck.main_section.entries
    return deck.sideboard_section.entries


def counts_map(entries: tuple[DeckCardEntry, ...]) -> dict[str, int]:
    """Quantités agrégées par nom Oracle anglais."""
    out: dict[str, int] = {}
    for entry in entries:
        out[entry.english_name] = out.get(entry.english_name, 0) + entry.quantity
    return out


def map_to_sorted_entries(quantities: Mapping[str, int]) -> tuple[DeckCardEntry, ...]:
    """Reconstruit des entrées triées (ordre déterministe)."""
    ordered = sorted(
        ((name, qty) for name, qty in quantities.items() if qty > 0),
        key=lambda item: (item[0].lower(), item[0]),
    )
    return tuple(DeckCardEntry(name, qty) for name, qty in ordered)


def with_replaced_section(
    deck: Deck,
    section: SectionChoice,
    new_entries: tuple[DeckCardEntry, ...],
) -> Deck:
    """Remplace une section par de nouvelles entrées."""
    if section == "main":
        return Deck.from_sections(DeckSection.main(new_entries), deck.sideboard_section)
    return Deck.from_sections(deck.main_section, DeckSection.sideboard(new_entries))


def total_copies_for_name(deck: Deck, english_name: str) -> int:
    """Somme main + sideboard pour un nom donné."""
    main_q = counts_map(deck.main_section.entries).get(english_name, 0)
    side_q = counts_map(deck.sideboard_section.entries).get(english_name, 0)
    return main_q + side_q


def classify_impact(
    score_before: float | None,
    score_after: float | None,
    *,
    epsilon: float = 1e-9,
) -> MutationImpact:
    """Compare deux scores pour étiqueter l'impact heuristique."""
    if score_before is None or score_after is None:
        return "neutral"
    if score_after > score_before + epsilon:
        return "beneficial"
    if score_after < score_before - epsilon:
        return "degrading"
    return "neutral"


def build_mutation_result(
    *,
    operator_id: str,
    deck_before: Deck,
    deck_after: Deck,
    mutations_applied: tuple[DeckMutation, ...],
    justification: str,
    format_definition: FormatDefinition,
    score_fn: Callable[[Deck], float] | None,
) -> DeckMutationResult:
    """Valide avant / après, calcule l'impact optionnel et retourne le résultat."""
    validation_before = format_definition.validate(deck_before)
    validation_after = format_definition.validate(deck_after)
    before_score = score_fn(deck_before) if score_fn is not None else None
    after_score = score_fn(deck_after) if score_fn is not None else None
    impact = classify_impact(before_score, after_score)
    return DeckMutationResult(
        operator_id=operator_id,
        deck_before=deck_before,
        deck_after=deck_after,
        mutations_applied=mutations_applied,
        justification=justification,
        validation_report_before=validation_before,
        validation_report_after=validation_after,
        impact=impact,
    )


def assert_main_at_least_minimum(deck: Deck, format_definition: FormatDefinition) -> None:
    """Vérifie la taille minimale du main pour le format supporté."""
    minimum = main_minimum_for_format(format_definition)
    if deck.main_total_quantity < minimum:
        raise DeckMutationException(
            f"Le main ne peut pas descendre sous {minimum} cartes pour ce format "
            f"(actuel : {deck.main_total_quantity})."
        )


def assert_pool_covers_name(deck: Deck, pool: CardPool, english_name: str) -> None:
    """Vérifie que le deck ne dépasse pas la disponibilité pool pour un nom."""
    used = total_copies_for_name(deck, english_name)
    available = pool.quantity_available(english_name)
    if available is None:
        return
    if used > available:
        raise DeckMutationException(
            f"Le pool ne permet pas {used} exemplaire(s) de « {english_name} » "
            f"(disponible : {available})."
        )


def assert_constructed_nonbasic_cap(deck: Deck, format_definition: FormatDefinition) -> None:
    """Applique la règle des exemplaires max hors bases sur le main (Construit MVP)."""
    if not isinstance(format_definition, ConstructedFormatDefinition):
        return
    cap = format_definition.max_copies_excluding_basic_lands
    basics = format_definition.basic_land_oracle_names
    main_counts = counts_map(deck.main_section.entries)
    for name, qty in main_counts.items():
        if name in basics:
            continue
        if qty > cap:
            raise DeckMutationException(
                f"Après mutation, « {name} » compterait {qty} exemplaire(s) au main "
                f"(maximum {cap} hors terrains de base)."
            )


def mutate_section_quantities(
    deck: Deck,
    section: SectionChoice,
    mutator: Callable[[MutableMapping[str, int]], None],
) -> Deck:
    """Copie les quantités de la section, applique ``mutator``, reconstruit le deck."""
    quantities: dict[str, int] = dict(counts_map(section_entries(deck, section)))
    mutator(quantities)
    new_entries = map_to_sorted_entries(quantities)
    return with_replaced_section(deck, section, new_entries)
