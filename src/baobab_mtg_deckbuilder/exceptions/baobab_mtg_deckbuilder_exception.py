"""Base exception type for the baobab-mtg-deckbuilder library."""


class BaobabMtgDeckbuilderException(Exception):
    """Root exception for all domain errors raised by this library.

    Concrete modules should raise specialized subclasses
    (:class:`~baobab_mtg_deckbuilder.exceptions.deck_validation_exception.DeckValidationException`,
    etc.) so callers can handle failures precisely while still allowing a
    broad ``except BaobabMtgDeckbuilderException`` when appropriate.

    :param args: Values forwarded to :class:`Exception` (typically a message).
    :type args: object
    """
