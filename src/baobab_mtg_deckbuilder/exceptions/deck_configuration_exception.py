"""Configuration-related domain errors."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckConfigurationException(BaobabMtgDeckbuilderException):
    """Raised when user or library configuration is invalid or inconsistent.

    Prefer this over :class:`ValueError` for structured handling of
    configuration mistakes at API boundaries.

    :param args: Values forwarded to :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
