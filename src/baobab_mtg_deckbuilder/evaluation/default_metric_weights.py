"""Poids par défaut des métriques heuristiques (miroir documenté dans ``pyproject.toml``)."""

from __future__ import annotations

# Identifiants alignés sur les attributs ``METRIC_ID`` des évaluateurs.
_DEFAULT_WEIGHTS: dict[str, float] = {
    "mana_curve_similarity": 0.2,
    "main_land_ratio": 0.2,
    "wubrg_color_balance": 0.2,
    "mana_data_consistency": 0.2,
    "card_type_diversity": 0.2,
}


def default_metric_weights() -> dict[str, float]:
    """Retourne une copie des poids par défaut (somme = ``1.0``).

    Les valeurs sont dupliquées sous
    ``[tool.baobab_mtg_deckbuilder.evaluation.default_metric_weights]`` dans
    ``pyproject.toml`` pour documentation et contrôle hors runtime.

    :returns: Table ``metric_id → poids`` (poids strictement positifs).
    :rtype: dict[str, float]
    """
    return dict(_DEFAULT_WEIGHTS)


def default_metric_weight_items() -> tuple[tuple[str, float], ...]:
    """Poids par défaut triés par ``metric_id`` (ordre déterministe).

    :returns: Paires ``(metric_id, poids)``.
    :rtype: tuple[tuple[str, float], ...]
    """
    return tuple(sorted(_DEFAULT_WEIGHTS.items(), key=lambda item: (item[0].lower(), item[0])))
