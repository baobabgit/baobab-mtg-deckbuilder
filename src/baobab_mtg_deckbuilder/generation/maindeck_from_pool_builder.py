"""Construction d'un main deck à partir d'un pool (Construit / Limité MVP)."""

from __future__ import annotations

import random
from typing import Literal, TypeAlias

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_generation_exception import DeckGenerationException
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition
from baobab_mtg_deckbuilder.validation.limited_format_definition import LimitedFormatDefinition

_THEORETICAL_GENERATION_CAP = 9999

CardPriority: TypeAlias = Literal["alphabetical", "scarce_first"]


def _effective_quantity(available_quantity: int | None) -> int:
    """Borne pratique pour les entrées catalogue à quantité indéfinie."""
    return _THEORETICAL_GENERATION_CAP if available_quantity is None else available_quantity


def _main_minimum_cards(format_definition: FormatDefinition) -> int:
    if isinstance(format_definition, ConstructedFormatDefinition):
        return format_definition.main_minimum_cards
    if isinstance(format_definition, LimitedFormatDefinition):
        return format_definition.main_minimum_cards
    raise DeckGenerationException(
        "Format non pris en charge pour la génération automatique : "
        f"{type(format_definition).__name__!r}."
    )


def _sort_name_key(name: str) -> tuple[str, str]:
    return (name.lower(), name)


def _order_pairs(
    pairs: list[tuple[str, int]],
    *,
    priority: CardPriority,
) -> None:
    """Trie la liste en place selon la priorité métier."""
    if priority == "scarce_first":
        pairs.sort(key=lambda item: (item[1], item[0].lower(), item[0]))
    else:
        pairs.sort(key=lambda item: _sort_name_key(item[0]))


def _rotate(pairs: list[tuple[str, int]], offset: int) -> None:
    """Rotation stable pour diversifier les candidats gloutons."""
    if not pairs or offset == 0:
        return
    k = offset % len(pairs)
    if k:
        pairs[:] = pairs[k:] + pairs[:k]


def _deck_from_main_counts(main_counts: dict[str, int]) -> Deck:
    ordered = sorted(main_counts.items(), key=lambda item: _sort_name_key(item[0]))
    entries = tuple(DeckCardEntry(name, qty) for name, qty in ordered if qty > 0)
    return Deck.from_sections(DeckSection.main(entries), DeckSection.sideboard(()))


def _consume_nonbasics_constructed(
    nonbasics: list[tuple[str, int]],
    *,
    remaining: dict[str, int],
    main_counts: dict[str, int],
    main_min: int,
    max_copies: int,
    initial_total: int,
) -> int:
    total = initial_total
    for name, _ in nonbasics:
        if total >= main_min:
            break
        pool_left = remaining.get(name, 0)
        if pool_left <= 0:
            continue
        already = main_counts.get(name, 0)
        cap_room = max_copies - already
        if cap_room <= 0:
            continue
        take = min(pool_left, cap_room, main_min - total)
        if take > 0:
            main_counts[name] = already + take
            remaining[name] = pool_left - take
            total += take
    return total


def _constructed_remaining_and_sections(
    pool: CardPool,
    basics_set: frozenset[str],
) -> tuple[dict[str, int], list[tuple[str, int]], list[tuple[str, int]]]:
    remaining: dict[str, int] = {
        entry.english_oracle_name: _effective_quantity(entry.available_quantity)
        for entry in pool.entries
    }
    nonbasics = [(name, remaining[name]) for name in remaining if name not in basics_set]
    basics = [(name, remaining[name]) for name in remaining if name in basics_set]
    return remaining, nonbasics, basics


def _limited_remaining_and_items(
    pool: CardPool,
) -> tuple[dict[str, int], list[tuple[str, int]]]:
    remaining = {
        entry.english_oracle_name: _effective_quantity(entry.available_quantity)
        for entry in pool.entries
    }
    items = [(name, remaining[name]) for name in remaining]
    return remaining, items


def _consume_basics_constructed(
    basics: list[tuple[str, int]],
    *,
    remaining: dict[str, int],
    main_counts: dict[str, int],
    main_min: int,
    initial_total: int,
) -> int:
    total = initial_total
    for name, _ in basics:
        if total >= main_min:
            break
        pool_left = remaining.get(name, 0)
        if pool_left <= 0:
            continue
        take = min(pool_left, main_min - total)
        if take > 0:
            already = main_counts.get(name, 0)
            main_counts[name] = already + take
            remaining[name] = pool_left - take
            total += take
    return total


def _fill_constructed_maindeck(
    pool: CardPool,
    fmt: ConstructedFormatDefinition,
    *,
    rng: random.Random,
    shuffle_nonbasics: bool,
    shuffle_basics: bool,
    nonbasic_priority: CardPriority,
    candidate_index: int,
    apply_list_rotation: bool,
) -> Deck:
    main_min = fmt.main_minimum_cards
    max_copies = fmt.max_copies_excluding_basic_lands
    remaining, nonbasics, basics = _constructed_remaining_and_sections(
        pool,
        fmt.basic_land_oracle_names,
    )

    _order_pairs(nonbasics, priority=nonbasic_priority)
    if shuffle_nonbasics:
        rng.shuffle(nonbasics)
    elif apply_list_rotation:
        _rotate(nonbasics, candidate_index)

    _order_pairs(basics, priority="alphabetical")
    if shuffle_basics:
        rng.shuffle(basics)
    elif apply_list_rotation:
        _rotate(basics, candidate_index)

    main_counts: dict[str, int] = {}
    total = _consume_nonbasics_constructed(
        nonbasics,
        remaining=remaining,
        main_counts=main_counts,
        main_min=main_min,
        max_copies=max_copies,
        initial_total=0,
    )
    total = _consume_basics_constructed(
        basics,
        remaining=remaining,
        main_counts=main_counts,
        main_min=main_min,
        initial_total=total,
    )

    if total < main_min:
        raise DeckGenerationException(
            f"Pool insuffisant pour atteindre un main de {main_min} cartes "
            f"(couvert pendant la construction : {total})."
        )

    return _deck_from_main_counts(main_counts)


def _consume_limited_items(
    items: list[tuple[str, int]],
    *,
    remaining: dict[str, int],
    main_min: int,
) -> tuple[dict[str, int], int]:
    main_counts: dict[str, int] = {}
    total = 0
    for name, _ in items:
        if total >= main_min:
            break
        pool_left = remaining.get(name, 0)
        if pool_left <= 0:
            continue
        already = main_counts.get(name, 0)
        take = min(pool_left, main_min - total)
        if take > 0:
            main_counts[name] = already + take
            remaining[name] = pool_left - take
            total += take
    return main_counts, total


def _fill_limited_maindeck(
    pool: CardPool,
    fmt: LimitedFormatDefinition,
    *,
    rng: random.Random,
    shuffle_cards: bool,
    card_priority: CardPriority,
    candidate_index: int,
    apply_list_rotation: bool,
) -> Deck:
    main_min = fmt.main_minimum_cards
    remaining, items = _limited_remaining_and_items(pool)

    _order_pairs(items, priority=card_priority)
    if shuffle_cards:
        rng.shuffle(items)
    elif apply_list_rotation:
        _rotate(items, candidate_index)

    main_counts, total = _consume_limited_items(
        items,
        remaining=remaining,
        main_min=main_min,
    )

    if total < main_min:
        raise DeckGenerationException(
            f"Pool insuffisant pour atteindre un main de {main_min} cartes "
            f"(couvert pendant la construction : {total})."
        )

    return _deck_from_main_counts(main_counts)


def build_maindeck_candidate(
    pool: CardPool,
    format_definition: FormatDefinition,
    *,
    rng: random.Random,
    shuffle_nonbasics: bool,
    shuffle_basics: bool,
    nonbasic_priority: CardPriority,
    candidate_index: int,
    apply_list_rotation: bool,
) -> Deck:
    """Construit un deck dont le sideboard est vide et le main est rempli depuis le pool.

    :param pool: Cartes disponibles (quantités ``None`` bornées en interne).
    :type pool: CardPool
    :param format_definition: Format Construit ou Limité MVP.
    :type format_definition: FormatDefinition
    :param rng: Générateur pseudo-aléatoire (mélanges).
    :type rng: random.Random
    :param shuffle_nonbasics: Mélanger l'ordre des non-bases (Construit) ou des cartes (Limité).
    :type shuffle_nonbasics: bool
    :param shuffle_basics: Mélanger l'ordre des terrains de base (Construit uniquement).
    :type shuffle_basics: bool
    :param nonbasic_priority: Ordre avant mélange / rotation (Construit et Limité).
    :type nonbasic_priority: CardPriority
    :param candidate_index: Indice du candidat (rotation gloutonne).
    :type candidate_index: int
    :param apply_list_rotation: Appliquer une rotation d'ordre pour diversifier sans mélange.
    :type apply_list_rotation: bool
    :returns: Deck avec main rempli et sideboard vide.
    :rtype: Deck
    :raises DeckGenerationException: Si le format n'est pas supporté ou le pool est trop petit.
    """
    if isinstance(format_definition, ConstructedFormatDefinition):
        return _fill_constructed_maindeck(
            pool,
            format_definition,
            rng=rng,
            shuffle_nonbasics=shuffle_nonbasics,
            shuffle_basics=shuffle_basics,
            nonbasic_priority=nonbasic_priority,
            candidate_index=candidate_index,
            apply_list_rotation=apply_list_rotation,
        )
    if isinstance(format_definition, LimitedFormatDefinition):
        return _fill_limited_maindeck(
            pool,
            format_definition,
            rng=rng,
            shuffle_cards=shuffle_nonbasics or shuffle_basics,
            card_priority=nonbasic_priority,
            candidate_index=candidate_index,
            apply_list_rotation=apply_list_rotation,
        )
    raise DeckGenerationException(
        "Format non pris en charge pour la génération automatique : "
        f"{type(format_definition).__name__!r}."
    )


def main_minimum_for_format(format_definition: FormatDefinition) -> int:
    """Expose le minimum de cartes au main attendu par le format (API utilitaire).

    :param format_definition: Définition de format supportée.
    :type format_definition: FormatDefinition
    :returns: Taille minimale du main.
    :rtype: int
    :raises DeckGenerationException: Si le format n'est pas supporté.
    """
    return _main_minimum_cards(format_definition)
