"""Tests for default metric weights."""

import pytest

from baobab_mtg_deckbuilder.evaluation.default_metric_weights import (
    default_metric_weight_items,
    default_metric_weights,
)


class TestDefaultMetricWeights:
    """Poids par défaut et déterminisme."""

    def test_sum_is_one(self) -> None:
        """Les cinq métriques somment à 1."""
        weights = default_metric_weights()
        assert sum(weights.values()) == pytest.approx(1.0)

    def test_sorted_items_match_dict(self) -> None:
        """Les items triés recouvrent le même ensemble."""
        d = default_metric_weights()
        items = default_metric_weight_items()
        assert dict(items) == d
        ids = [i[0] for i in items]
        assert ids == sorted(ids, key=lambda x: (x.lower(), x))
