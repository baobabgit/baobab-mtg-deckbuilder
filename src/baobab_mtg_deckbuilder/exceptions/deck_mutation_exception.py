"""Erreurs métier liées aux mutations de deck."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckMutationException(BaobabMtgDeckbuilderException):
    """Levée lorsqu'une mutation ne peut pas être appliquée de façon cohérente.

    Exemples : carte absente de la zone ciblée, pool insuffisant, violation des
    règles de format après transformation, ou données analytiques manquantes.

    :param args: Valeurs transmises à :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
