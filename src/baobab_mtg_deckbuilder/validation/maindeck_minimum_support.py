"""Logique partagée pour les règles de taille minimale du main deck."""

from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)


def issues_when_main_below_minimum(
    total: int,
    minimum_cards: int,
    *,
    error_code: str,
    message: str,
    suggestion: str,
    affected_entity: str = "main",
) -> tuple[DeckValidationIssue, ...]:
    """Retourne une erreur si ``total`` < ``minimum_cards``, sinon un tuple vide.

    :param total: Nombre de cartes actuellement dans le main.
    :type total: int
    :param minimum_cards: Seuil minimal attendu.
    :type minimum_cards: int
    :param error_code: Code machine de l'issue.
    :type error_code: str
    :param message: Texte décrivant le problème.
    :type message: str
    :param suggestion: Piste de correction.
    :type suggestion: str
    :param affected_entity: Entité affectée (défaut ``main``).
    :type affected_entity: str
    :returns: Zéro ou une issue d'erreur.
    :rtype: tuple[DeckValidationIssue, ...]
    """
    if total >= minimum_cards:
        return ()
    return (
        DeckValidationIssue(
            severity=DeckValidationIssueSeverity.ERROR,
            code=error_code,
            message=message,
            affected_entity=affected_entity,
            suggestion=suggestion,
        ),
    )
