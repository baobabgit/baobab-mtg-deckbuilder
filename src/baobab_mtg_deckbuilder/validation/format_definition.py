"""Définition abstraite d'un format de jeu et validation associée."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_constraint_set import DeckConstraintSet
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_report import DeckValidationReport
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule


class FormatDefinition(ABC):
    """Point d'entrée pour décrire un format (contraintes déclaratives + règles).

    Les sous-classes fournissent un :class:`DeckConstraintSet` documentaire et
    un jeu de :class:`DeckValidationRule` exécutables.
    """

    @property
    @abstractmethod
    def format_key(self) -> str:
        """Clé stable du format (ex. ``constructed_mvp``)."""

    @abstractmethod
    def constraint_set(self) -> DeckConstraintSet:
        """Contraintes déclaratives présentées aux utilisateurs."""

    @abstractmethod
    def validation_rules(self) -> tuple[DeckValidationRule, ...]:
        """Règles évaluées dans l'ordre retourné."""

    def validate(self, deck: Deck) -> DeckValidationReport:
        """Exécute toutes les règles et retourne un rapport trié.

        :param deck: Deck à contrôler.
        :type deck: Deck
        :returns: Rapport agrégé.
        :rtype: DeckValidationReport
        """
        collected: list[DeckValidationIssue] = []
        for rule in self.validation_rules():
            collected.extend(rule.evaluate(deck))
        return DeckValidationReport.from_issues(tuple(collected))
