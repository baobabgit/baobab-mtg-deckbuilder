# baobab-mtg-deckbuilder

Bibliothèque Python pour **construire**, **valider**, **évaluer**, **comparer** et **optimiser** des decks [Magic: The Gathering](https://magic.wizards.com/) à partir d’un pool de cartes, de contraintes de format et d’objectifs d’optimisation.

La librairie reste **métier pure** : pas de dépendance à une API web ni à un front. Les sorties sont pensées pour être **typées**, **explicables** et **testables**.

## Installation (développement)

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Utilisation minimale

```python
import baobab_mtg_deckbuilder as bd

print(bd.__version__)

# Modèle de deck (main + sideboard, immuable)
main = bd.DeckSection.main(
    [
        bd.DeckCardEntry("Lightning Bolt", 4),
        bd.DeckCardEntry("Mountain", 20),
    ]
)
side = bd.DeckSection.sideboard([bd.DeckCardEntry("Pyroblast", 2)])
deck = bd.Deck.from_sections(main, side)
print(deck.total_quantity, deck.summary().main_quantity_by_english_name)

# Validation structurelle MVP (Construit / Limité)
fmt = bd.ConstructedFormatDefinition()
report = fmt.validate(deck)
print(report.is_valid, report.error_count, report.warning_count, report.info_count)

# Pool catalogue / collection (protocoles, sans API externe)
class MyCatalog:
    def iter_theoretical_entries(self) -> tuple[bd.CardPoolEntry, ...]:
        return (bd.CardPoolEntry("Lightning Bolt", None),)

pool = bd.CardPool.from_catalog(MyCatalog())
print(pool.is_theoretical, pool.quantity_available("Lightning Bolt"))

# Statistiques analytiques (métadonnées injectées via un protocole)
class MyAnalyticProvider:
    def analytic_profile_for(self, name: str) -> bd.CardAnalyticProfile | None:
        if name == "Lightning Bolt":
            return bd.CardAnalyticProfile(
                mana_value=1,
                is_land=False,
                color_identity=frozenset({"R"}),
                type_categories=frozenset({"Instant"}),
            )
        if name == "Mountain":
            return bd.CardAnalyticProfile(
                mana_value=0,
                is_land=True,
                color_identity=frozenset({"R"}),
                type_categories=frozenset({"Land"}),
            )
        return None

stats = bd.DeckStatistics.analyze(deck, MyAnalyticProvider())
print(stats.main_spell_mana_curve, stats.main_land_quantity)

# Métriques heuristiques (indépendantes du moteur de règles)
curve_m = bd.ManaCurveEvaluator().evaluate(stats)
lands_m = bd.LandRatioEvaluator().evaluate(stats)
print(curve_m.normalized_score, curve_m.explanation.summary)
print(lands_m.metric_id, lands_m.raw_score)

# Score agrégé pondéré (breakdown + explication de composition)
metrics = (
    curve_m,
    lands_m,
    bd.ColorBalanceEvaluator().evaluate(stats),
    bd.ManaBaseConsistencyEvaluator().evaluate(stats),
    bd.CardTypeBalanceEvaluator().evaluate(stats),
)
evaluation = bd.WeightedScoreAggregator().aggregate(metrics)
print(evaluation.score.final_score, evaluation.explanation.summary)

# Génération de candidats (pool + format, graine, plusieurs decks)
constructed = bd.ConstructedFormatDefinition()
entries = tuple(
    bd.CardPoolEntry(f"Nonbasic {i:02d}", 4) for i in range(15)
)
pool = bd.CardPool.from_entries(entries, pool_kind="physical")
req = bd.DeckGenerationRequest(
    format_definition=constructed,
    pool=pool,
    random_seed=42,
    candidate_count=3,
)
result = bd.GreedyGenerationStrategy().generate(req)
print(result.strategy_key, all(c.is_valid for c in result.candidates))

# Hiérarchie d'exceptions (à utiliser pour les erreurs métier)
raise bd.DeckValidationException("exemple : deck illégal")
```

## Qualité et tests

Les réglages sont centralisés dans `pyproject.toml` (black, pylint, mypy, flake8, bandit, pytest, coverage).

```bash
python -m black --check .
python -m flake8 .
python -m mypy src tests
python -m pylint src tests
python -m bandit -r src
python -m pytest
```

La couverture HTML et XML est générée sous `docs/tests/coverage/` (voir `docs/tests/coverage/README.md`).

## Build wheel / sdist

```bash
python -m pip install "build>=1.0.0,<2.0.0"
python -m build
```

## Contribution

- Branches de fonctionnalité : `feature/...`
- Messages de commit : [Conventional Commits](https://www.conventionalcommits.org/)
- Contraintes détaillées : `docs/000_dev_constraints.md`

## Licence

MIT — voir le fichier `LICENSE`.
