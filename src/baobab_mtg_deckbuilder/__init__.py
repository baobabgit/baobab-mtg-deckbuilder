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
from baobab_mtg_deckbuilder.deck import (
    MAIN_DECK_SECTION_ID,
    SIDEBOARD_SECTION_ID,
    Deck,
    DeckCardEntry,
    DeckListView,
    DeckSection,
    DeckSummary,
)
from baobab_mtg_deckbuilder.deck import __all__ as _DECK_ALL
from baobab_mtg_deckbuilder.exceptions import __all__ as _EXCEPTIONS_ALL
from baobab_mtg_deckbuilder.pool import (
    CardPool,
    CardPoolEntry,
    CatalogCardProviderProtocol,
    CollectionPoolProviderProtocol,
)
from baobab_mtg_deckbuilder.pool import __all__ as _POOL_ALL
from baobab_mtg_deckbuilder.validation import (
    DEFAULT_BASIC_LAND_ORACLE_NAMES,
    ConstructedFormatDefinition,
    ConstructedMaindeckMinimumSizeRule,
    ConstructedNonbasicMaxCopiesRule,
    ConstructedSideboardMaximumSizeRule,
    DeckConstraint,
    DeckConstraintSet,
    DeckValidationIssue,
    DeckValidationIssueSeverity,
    DeckValidationReport,
    DeckValidationRule,
    FormatDefinition,
    LimitedFormatDefinition,
    LimitedMaindeckMinimumSizeRule,
    LimitedSideboardInformationRule,
    LimitedSideboardSizeWarningRule,
)
from baobab_mtg_deckbuilder.validation import __all__ as _VALIDATION_ALL

try:
    __version__: str = version("baobab-mtg-deckbuilder")
except PackageNotFoundError:
    __version__ = "0.4.0"

__all__ = ["__version__", *_EXCEPTIONS_ALL, *_DECK_ALL, *_VALIDATION_ALL, *_POOL_ALL]
