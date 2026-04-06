"""Baobab MTG Deckbuilder — construction et optimisation de decks Magic: The Gathering."""

from importlib.metadata import PackageNotFoundError, version

from baobab_mtg_deckbuilder.exceptions import (
    BaobabMtgDeckbuilderException,
    DeckConfigurationException,
    DeckGenerationException,
    DeckOptimizationException,
    DeckSimulationException,
    DeckValidationException,
)
from baobab_mtg_deckbuilder.exceptions import __all__ as _EXCEPTIONS_ALL

try:
    __version__: str = version("baobab-mtg-deckbuilder")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = ["__version__", *_EXCEPTIONS_ALL]
