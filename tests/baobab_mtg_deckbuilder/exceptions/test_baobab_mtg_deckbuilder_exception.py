"""Tests for :class:`BaobabMtgDeckbuilderException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)


class TestBaobabMtgDeckbuilderException:
    """Tests for the base project exception."""

    def test_is_exception_subclass(self) -> None:
        """The base type subclasses :class:`Exception`."""
        assert issubclass(BaobabMtgDeckbuilderException, Exception)

    def test_can_raise_and_catch_with_message(self) -> None:
        """Raising with a message preserves ``args``."""
        with pytest.raises(BaobabMtgDeckbuilderException) as exc_info:
            raise BaobabMtgDeckbuilderException("failure")
        assert exc_info.value.args == ("failure",)
