"""Quantités dérivées pour les heuristiques.

Basées sur
:class:`~baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result.DeckStatisticsResult`.
"""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult


def main_deck_card_quantity(stats: DeckStatisticsResult) -> int:
    """Nombre total de cartes dans le main (toutes sections confondues du modèle)."""
    return sum(stats.main_quantity_by_english_name.values())


def main_nonland_spell_quantity(stats: DeckStatisticsResult) -> int:
    """Exemplaires de sorts non-terrain pris en compte dans la courbe ou en CMC inconnu."""
    curve = stats.main_spell_mana_curve
    return sum(curve.values()) + stats.main_spell_mana_value_unknown_quantity
