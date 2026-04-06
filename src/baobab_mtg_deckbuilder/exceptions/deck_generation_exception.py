"""Deck generation-related domain errors."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckGenerationException(BaobabMtgDeckbuilderException):
    """Raised when automatic deck construction cannot complete successfully.

    Typical causes include an empty pool, unsatisfiable constraints, or
    exhausted search budgets.

    :param args: Values forwarded to :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
