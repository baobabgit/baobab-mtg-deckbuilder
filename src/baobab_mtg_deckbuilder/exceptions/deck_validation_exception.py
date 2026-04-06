"""Validation-related domain errors."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckValidationException(BaobabMtgDeckbuilderException):
    """Raised when a deck violates format rules or validation constraints.

    Use this type for legality checks, size limits, and other structural
    validation failures before evaluation or optimization.

    :param args: Values forwarded to :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
