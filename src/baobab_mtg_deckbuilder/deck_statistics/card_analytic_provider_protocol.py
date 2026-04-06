"""Protocole : résolution d'un profil analytique par nom anglais Oracle."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile


@runtime_checkable
class CardAnalyticProviderProtocol(Protocol):
    """Fournit un :class:`CardAnalyticProfile` pour un nom de carte du deck."""

    def analytic_profile_for(self, english_name: str) -> CardAnalyticProfile | None:
        """Retourne le profil pour ``english_name``, ou ``None`` si inconnu.

        :param english_name: Nom anglais Oracle (déjà normalisé côté :class:`DeckCardEntry`).
        :type english_name: str
        :returns: Profil ou ``None``.
        :rtype: CardAnalyticProfile | None
        """
        ...  # pylint: disable=unnecessary-ellipsis
