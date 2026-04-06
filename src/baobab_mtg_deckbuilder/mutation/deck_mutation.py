"""Enregistrement atomique d'une transformation appliquée au deck."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeckMutation:
    """Description typée d'un changement unitaire (traçabilité / logs).

    :param mutation_code: Identifiant stable machine (ex. ``replace_card``).
    :type mutation_code: str
    :param message: Explication courte orientée humain.
    :type message: str
    :param section_identifier: Zone concernée (``main`` ou ``sideboard``).
    :type section_identifier: str
    """

    mutation_code: str
    message: str
    section_identifier: str
