"""Baobab MTG Deckbuilder — construction et optimisation de decks Magic: The Gathering."""

from importlib.metadata import PackageNotFoundError, version

from baobab_mtg_deckbuilder.exceptions import (
    BaobabMtgDeckbuilderException,
    DeckConfigurationException,
    DeckEvaluationException,
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
from baobab_mtg_deckbuilder.deck_statistics import (
    MANA_CURVE_CAP,
    CardAnalyticProfile,
    CardAnalyticProviderProtocol,
    DeckStatistics,
    DeckStatisticsResult,
)
from baobab_mtg_deckbuilder.deck_statistics import __all__ as _DECK_STATISTICS_ALL
from baobab_mtg_deckbuilder.evaluation import (
    CardTypeBalanceEvaluator,
    ColorBalanceEvaluator,
    DeckEvaluation,
    DeckEvaluationBreakdown,
    DeckEvaluationBreakdownLine,
    DeckEvaluationExplanation,
    DeckMetric,
    DeckScore,
    LandRatioEvaluator,
    ManaBaseConsistencyEvaluator,
    ManaCurveEvaluator,
    WeightedScoreAggregator,
    default_metric_weight_items,
    default_metric_weights,
    main_deck_card_quantity,
    main_nonland_spell_quantity,
)
from baobab_mtg_deckbuilder.evaluation import __all__ as _EVALUATION_ALL
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
    __version__ = "0.7.0"

__all__ = [
    "__version__",
    *_EXCEPTIONS_ALL,
    *_DECK_ALL,
    *_DECK_STATISTICS_ALL,
    *_EVALUATION_ALL,
    *_VALIDATION_ALL,
    *_POOL_ALL,
]
