"""Formats, contraintes et validation structurelle des decks."""

from baobab_mtg_deckbuilder.validation.basic_land_oracle_names import (
    DEFAULT_BASIC_LAND_ORACLE_NAMES,
)
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from baobab_mtg_deckbuilder.validation.constructed_maindeck_minimum_size_rule import (
    ConstructedMaindeckMinimumSizeRule,
)
from baobab_mtg_deckbuilder.validation.constructed_nonbasic_max_copies_rule import (
    ConstructedNonbasicMaxCopiesRule,
)
from baobab_mtg_deckbuilder.validation.constructed_sideboard_maximum_size_rule import (
    ConstructedSideboardMaximumSizeRule,
)
from baobab_mtg_deckbuilder.validation.deck_constraint import DeckConstraint
from baobab_mtg_deckbuilder.validation.deck_constraint_set import DeckConstraintSet
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_report import DeckValidationReport
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition
from baobab_mtg_deckbuilder.validation.limited_format_definition import (
    LimitedFormatDefinition,
)
from baobab_mtg_deckbuilder.validation.limited_maindeck_minimum_size_rule import (
    LimitedMaindeckMinimumSizeRule,
)
from baobab_mtg_deckbuilder.validation.limited_sideboard_information_rule import (
    LimitedSideboardInformationRule,
)
from baobab_mtg_deckbuilder.validation.limited_sideboard_size_warning_rule import (
    LimitedSideboardSizeWarningRule,
)

__all__ = [
    "DEFAULT_BASIC_LAND_ORACLE_NAMES",
    "ConstructedFormatDefinition",
    "ConstructedMaindeckMinimumSizeRule",
    "ConstructedNonbasicMaxCopiesRule",
    "ConstructedSideboardMaximumSizeRule",
    "DeckConstraint",
    "DeckConstraintSet",
    "DeckValidationIssue",
    "DeckValidationIssueSeverity",
    "DeckValidationReport",
    "DeckValidationRule",
    "FormatDefinition",
    "LimitedFormatDefinition",
    "LimitedMaindeckMinimumSizeRule",
    "LimitedSideboardInformationRule",
    "LimitedSideboardSizeWarningRule",
]
