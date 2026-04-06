"""Statistiques analytiques de deck (courbe de mana, couleurs, types, terrains)."""

from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from baobab_mtg_deckbuilder.deck_statistics.deck_statistics import (
    MANA_CURVE_CAP,
    DeckStatistics,
)
from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult

__all__ = [
    "MANA_CURVE_CAP",
    "CardAnalyticProfile",
    "CardAnalyticProviderProtocol",
    "DeckStatistics",
    "DeckStatisticsResult",
]
