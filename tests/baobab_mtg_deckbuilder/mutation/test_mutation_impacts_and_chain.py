"""Impact score, traçabilité, validation et chaînage léger."""

from baobab_mtg_deckbuilder.mutation.adjust_land_count_operator import AdjustLandCountOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_replacement_suggestion import DeckReplacementSuggestion
from baobab_mtg_deckbuilder.mutation.replace_card_operator import ReplaceCardOperator
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from tests.baobab_mtg_deckbuilder.mutation.constructed_deck_factory import sixty_spell_deck


class TestMutationImpactsAndChain:
    """Scénarios heuristiques d'optimisation."""

    def _ctx(
        self,
        deck,
        pool,
        *,
        score_fn=None,
    ) -> DeckMutationContext:
        fmt = ConstructedFormatDefinition()
        return DeckMutationContext(
            deck=deck,
            format_definition=fmt,
            pool=pool,
            score_fn=score_fn,
        )

    def test_beneficial_impact_when_score_increases(self) -> None:
        """Un score monotone sur la carte ajoutée détecte un gain."""
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))

        def score_fn(d):
            return float(d.summary().main_quantity_by_english_name.get("ExtraSpell", 0))

        ctx = self._ctx(deck, pool, score_fn=score_fn)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Ajouter ExtraSpell au main.",
        )
        result = ReplaceCardOperator(suggestion).apply(ctx)
        assert result.impact == "beneficial"

    def test_degrading_impact_when_score_decreases(self) -> None:
        """Baisser la quantité d'une carte suivie par le score = impact dégradant."""
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))

        def score_fn(d):
            return float(d.summary().main_quantity_by_english_name.get("Spell 00", 0))

        ctx = self._ctx(deck, pool, score_fn=score_fn)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Retirer un Spell 00.",
        )
        result = ReplaceCardOperator(suggestion).apply(ctx)
        assert result.impact == "degrading"

    def test_neutral_impact_without_score_fn(self) -> None:
        """Sans fonction de score, l'impact reste neutre par convention."""
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))
        ctx = self._ctx(deck, pool)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Remplacement neutre non mesuré.",
        )
        result = ReplaceCardOperator(suggestion).apply(ctx)
        assert result.impact == "neutral"

    def test_traceability_fields(self) -> None:
        """Avant/après distincts, journal et justification présents."""
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))
        ctx = self._ctx(deck, pool)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Traçabilité explicite.",
        )
        result = ReplaceCardOperator(suggestion).apply(ctx)
        assert result.deck_before is not result.deck_after
        assert (
            result.deck_before.list_view().main_entries
            != result.deck_after.list_view().main_entries
        )
        assert result.mutations_applied
        assert len(result.justification) > 0

    def test_validation_reports_match_direct_validate(self) -> None:
        """Les rapports portés par le résultat coïncident avec ``validate``."""
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))
        fmt = ConstructedFormatDefinition()
        ctx = DeckMutationContext(deck=deck, format_definition=fmt, pool=pool)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Cohérence validation.",
        )
        result = ReplaceCardOperator(suggestion).apply(ctx)
        assert result.validation_report_before.issues == fmt.validate(result.deck_before).issues
        assert result.validation_report_after.issues == fmt.validate(result.deck_after).issues

    def test_chain_two_operators(self) -> None:
        """L'optimiseur peut enchaîner sur ``deck_after``."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell", "Island"))
        ctx1 = DeckMutationContext(deck=deck, format_definition=fmt, pool=pool)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Chaînage : remplacement puis terrain.",
        )
        first = ReplaceCardOperator(suggestion).apply(ctx1)
        ctx2 = DeckMutationContext(
            deck=first.deck_after,
            format_definition=fmt,
            pool=pool,
        )
        second = AdjustLandCountOperator("Island", 1).apply(ctx2)
        assert second.validation_report_after.is_valid
        assert second.deck_after.main_total_quantity == first.deck_after.main_total_quantity + 1
