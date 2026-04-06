"""Noms anglais Oracle des terrains de base reconnus pour la règle des 4 exemplaires."""

from typing import Final

#: Ensemble minimal utilisé par la validation Construit MVP (hors extensions de liste).
DEFAULT_BASIC_LAND_ORACLE_NAMES: Final[frozenset[str]] = frozenset(
    {
        "Plains",
        "Island",
        "Swamp",
        "Mountain",
        "Forest",
        "Wastes",
        "Snow-Covered Plains",
        "Snow-Covered Island",
        "Snow-Covered Swamp",
        "Snow-Covered Mountain",
        "Snow-Covered Forest",
    }
)
