"""Erreurs liées à l'évaluation heuristique de deck."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckEvaluationException(BaobabMtgDeckbuilderException):
    """Levée lorsqu'une opération d'évaluation ne peut pas s'appliquer aux entrées données.

    Les métriques unitaires renvoient en général un score même si les données sont
    incomplètes ; cette exception sert aux orchestrations strictes (agrégation,
    pondération invalide, etc.).

    :param args: Valeurs transmises à :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
