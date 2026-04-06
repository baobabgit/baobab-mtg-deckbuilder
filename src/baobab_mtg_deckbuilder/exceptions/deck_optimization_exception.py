"""Optimization-related domain errors."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class DeckOptimizationException(BaobabMtgDeckbuilderException):
    """Raised when an optimization run fails in a domain-specific way.

    Examples include invalid objective configuration, non-convergence under
    configured limits, or inconsistent internal state during search.

    :param args: Values forwarded to :class:`BaobabMtgDeckbuilderException`.
    :type args: object
    """
