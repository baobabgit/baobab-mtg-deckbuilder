"""Format Construit MVP (60+ main, 4 max hors bases, side <= 15)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)
from baobab_mtg_deckbuilder.validation.basic_land_oracle_names import (
    DEFAULT_BASIC_LAND_ORACLE_NAMES,
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
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition


@dataclass(frozen=True, slots=True)
class ConstructedFormatDefinition(FormatDefinition):
    """Paramètres du format **Construit** pour la validation structurelle MVP.

    :param main_minimum_cards: Taille minimale du main (défaut 60).
    :type main_minimum_cards: int
    :param sideboard_maximum_cards: Taille maximale du sideboard (défaut 15).
    :type sideboard_maximum_cards: int
    :param max_copies_excluding_basic_lands: Exemplaires max par carte hors bases (défaut 4).
    :type max_copies_excluding_basic_lands: int
    :param basic_land_oracle_names: Terrains de base exclus de la règle des 4.
    :type basic_land_oracle_names: frozenset[str]

    :raises DeckConfigurationException: Si les paramètres sont incohérents.
    """

    main_minimum_cards: int = 60
    sideboard_maximum_cards: int = 15
    max_copies_excluding_basic_lands: int = 4
    basic_land_oracle_names: frozenset[str] = DEFAULT_BASIC_LAND_ORACLE_NAMES

    def __post_init__(self) -> None:
        if self.main_minimum_cards < 1:
            raise DeckConfigurationException(
                "main_minimum_cards doit être >= 1 pour le format construit."
            )
        if self.sideboard_maximum_cards < 0:
            raise DeckConfigurationException("sideboard_maximum_cards ne peut pas être négatif.")
        if self.max_copies_excluding_basic_lands < 1:
            raise DeckConfigurationException("max_copies_excluding_basic_lands doit être >= 1.")

    @property
    def format_key(self) -> str:
        return "constructed_mvp"

    def constraint_set(self) -> DeckConstraintSet:
        return DeckConstraintSet(
            format_key=self.format_key,
            constraints=(
                DeckConstraint(
                    code="CONSTRUCTED_MAIN_MIN",
                    summary="Main deck : nombre minimal de cartes.",
                    value=self.main_minimum_cards,
                ),
                DeckConstraint(
                    code="CONSTRUCTED_NONBASIC_MAX_COPIES",
                    summary=(
                        "Maximum d'exemplaires identiques hors terrains de base "
                        "(Oracle anglais)."
                    ),
                    value=self.max_copies_excluding_basic_lands,
                ),
                DeckConstraint(
                    code="CONSTRUCTED_SIDEBOARD_MAX",
                    summary="Sideboard : nombre maximal de cartes.",
                    value=self.sideboard_maximum_cards,
                ),
            ),
        )

    def validation_rules(self) -> tuple[DeckValidationRule, ...]:
        return (
            ConstructedMaindeckMinimumSizeRule(self.main_minimum_cards),
            ConstructedNonbasicMaxCopiesRule(
                self.basic_land_oracle_names,
                self.max_copies_excluding_basic_lands,
            ),
            ConstructedSideboardMaximumSizeRule(self.sideboard_maximum_cards),
        )
