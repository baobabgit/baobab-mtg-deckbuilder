"""Format Limité MVP (40+ cartes au main, info sideboard)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)
from baobab_mtg_deckbuilder.validation.deck_constraint import DeckConstraint
from baobab_mtg_deckbuilder.validation.deck_constraint_set import DeckConstraintSet
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition
from baobab_mtg_deckbuilder.validation.limited_maindeck_minimum_size_rule import (
    LimitedMaindeckMinimumSizeRule,
)
from baobab_mtg_deckbuilder.validation.limited_sideboard_information_rule import (
    LimitedSideboardInformationRule,
)
from baobab_mtg_deckbuilder.validation.limited_sideboard_size_warning_rule import (
    LimitedSideboardSizeWarningRule,
)


@dataclass(frozen=True, slots=True)
class LimitedFormatDefinition(FormatDefinition):
    """Paramètres du format **Limité** pour la validation structurelle MVP.

    :param main_minimum_cards: Taille minimale du main (défaut 40).
    :type main_minimum_cards: int

    :raises DeckConfigurationException: Si ``main_minimum_cards`` est invalide.
    """

    main_minimum_cards: int = 40

    def __post_init__(self) -> None:
        if self.main_minimum_cards < 1:
            raise DeckConfigurationException(
                "main_minimum_cards doit être >= 1 pour le format limité."
            )

    @property
    def format_key(self) -> str:
        return "limited_mvp"

    def constraint_set(self) -> DeckConstraintSet:
        return DeckConstraintSet(
            format_key=self.format_key,
            constraints=(
                DeckConstraint(
                    code="LIMITED_MAIN_MIN",
                    summary="Main deck limité : nombre minimal de cartes.",
                    value=self.main_minimum_cards,
                ),
            ),
        )

    def validation_rules(self) -> tuple[DeckValidationRule, ...]:
        return (
            LimitedMaindeckMinimumSizeRule(self.main_minimum_cards),
            LimitedSideboardInformationRule(),
            LimitedSideboardSizeWarningRule(),
        )
