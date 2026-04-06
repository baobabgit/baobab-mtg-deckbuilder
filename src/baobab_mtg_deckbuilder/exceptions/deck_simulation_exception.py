"""Simulation adapter-related domain errors."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckSimulationException(BaobabMtgDeckbuilderException):
    """Raised when a simulation integration step cannot be completed.

    This type covers adapter misconfiguration, unsupported scenarios, or
    failures propagated from a simulation backend in a library-controlled way.

    :param args: Values forwarded to :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
