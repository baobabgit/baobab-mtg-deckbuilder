"""Fournisseur analytique factice pour les tests."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile


@dataclass(frozen=True, slots=True)
class FakeCardAnalyticProvider:
    """Retourne des profils depuis un mapping nom → profil."""

    _profiles: dict[str, CardAnalyticProfile]

    def analytic_profile_for(self, english_name: str) -> CardAnalyticProfile | None:
        return self._profiles.get(english_name)
