# Journal de développement

Les entrées les plus récentes apparaissent en premier.

## 2026-04-06 (feature/mutation-operators)

### Modifications

- Ajout du paquet `mutation/` : résultats avec deck avant/après, rapports de validation, journal `DeckMutation`, justification textuelle ; opérateurs de remplacement (suggestion typée), ajustement ±1 d’un terrain de base MVP, correction de couleur via `CardAnalyticProviderProtocol`, échange main ↔ sideboard.
- `DeckMutationException` ; utilitaires internes `mutation_support` (contraintes pool / construit, classification d’impact) ; dépendance contrôlée à `main_minimum_for_format` pour les garde-fous de taille de main.
- Tests miroir (opérateurs, impacts, chaînage, validation, exception) ; version `0.9.0`, `README` / `CHANGELOG` / journal ; `flake8` `per-file-ignores` pour `mutation/__init__.py`.

### Buts

- Livrer la feature **09_mutation_operators** : transformations explicables et chaînables par un optimiseur, sans UI ni persistance.

### Impact

- Les moteurs de recherche pourront itérer sur `DeckMutationResult.deck_after` avec traçabilité (`mutations_applied`, `justification`, `impact`).

## 2026-04-06 (feature/generation-strategies)

### Modifications

- Ajout du paquet `generation/` : requête / résultat / candidat typés, `DeckGenerationStrategy` (ABC), stratégies gloutonne (ordre alphabétique + rotation), aléatoire semée, « contrainte » (rareté relative dans le pool), hybride pair/impair ; `build_maindeck_candidate` + `main_minimum_for_format`.
- Tests miroir (requête, candidat, builder, stratégies, reproductibilité, comparaison) ; extension des exports publics et de `test_package_imports` ; version `0.8.0`, `README` / `CHANGELOG` / journal ; `flake8` `per-file-ignores` pour `generation/__init__.py`.

### Buts

- Livrer la feature **08_generation_strategies** : premières constructions automatiques depuis un `CardPool` et un `FormatDefinition`, sorties structurées et validées, déterminisme contrôlé.

### Impact

- Les optimiseurs et pipelines pourront produire des populations de decks candidats sans couplage UI/API, avec traçabilité (`strategy_key`, `candidate_index`, rapport de validation par candidat).

## 2026-04-06 (feature/weighted-scoring)

### Modifications

- Ajout de l’agrégateur `WeightedScoreAggregator` (poids configurables, bonus / pénalité, `DeckScore`, `DeckEvaluationBreakdown` + lignes typées, `DeckEvaluation` avec explication de composition).
- `default_metric_weights` et tableau TOML miroir dans `pyproject.toml` ; tests d’alignement code / fichier projet.
- Version `0.7.0`, `README` / `CHANGELOG` / journal ; extension des exports publics et de `test_package_imports`.

### Buts

- Livrer la feature **07_weighted_scoring_and_explanations** : score global explicable, breakdown stable pour classement ou recommandation.

### Impact

- Les optimiseurs pourront composer un score unique tout en conservant la traçabilité par métrique.

## 2026-04-06 (feature/heuristic-evaluation)

### Modifications

- Ajout du paquet `evaluation/` : `DeckMetric`, `DeckEvaluationExplanation`, cinq évaluateurs (courbe vs gabarit L1, ratio terrains cible 38 %, entropie WUBRG, cohérence multiplicative profils/CMC/couleurs « ? », diversité des types avec score modéré mono-type), helpers `heuristic_inputs`.
- `DeckEvaluationException` + test d’héritage ; fabrique de tests `deck_statistics_result` ; extension des imports publics et de `test_package_imports` ; version `0.6.0`, `README` / `CHANGELOG` / journal ; `flake8` `per-file-ignores` pour `evaluation/__init__.py`.

### Buts

- Livrer la feature **06_heuristic_evaluation_metrics** : premières métriques explicables sans simulation ni moteur de validation, pondérables via `metric_id` / `normalized_score`.

### Impact

- L’optimisation et l’UI pourront composer des scores à partir de `DeckStatisticsResult` + évaluateurs indépendants.

## 2026-04-06 (feature/deck-statistics)

### Modifications

- Ajout du paquet `deck_statistics/` : `CardAnalyticProfile`, `CardAnalyticProviderProtocol`, `DeckStatistics.analyze`, `DeckStatisticsResult`, `MANA_CURVE_CAP` ; règles déterministes documentées (terrain via `is_land` ou type `Land`, courbe sur sorts non-terrain, couleurs et types avec repli `?`, profils absents comptés à part).
- Tests miroir + `FakeCardAnalyticProvider` ; extension des exports publics et du test de version fallback ; `0.5.0`, `README` / `CHANGELOG` / journal ; `flake8` `per-file-ignores` pour `deck_statistics/__init__.py`.

### Buts

- Livrer la feature **05_deck_statistics_and_aggregates** : agrégats réutilisables pour validation, évaluation et explicabilité, sans couplage aux stratégies d’optimisation.

### Impact

- Les pipelines pourront consommer un snapshot typé (courbe, couleurs, types, terrains, copies) en branchant un fournisseur de profils sur n’importe quelle source de données carte.

## 2026-04-06 (feature/pool-protocols)

### Modifications

- Ajout du paquet `pool/` : `CardPoolEntry` (nom Oracle anglais, quantité entière ou `None` pour non borné côté catalogue), `CardPool` immuable (`is_theoretical`, entrées fusionnées et triées), fabriques `from_catalog` / `from_collection` / `from_entries`, méthodes `lookup`, `quantity_available`, `distinct_card_count`.
- Fusion théorique : `None` domine sur un même nom ; fusion collection : somme des entiers, `DeckConfigurationException` si quantité `None`.
- Protocoles strictement typés et `runtime_checkable` : `CatalogCardProviderProtocol`, `CollectionPoolProviderProtocol`.
- Tests miroir + fakes `FakeCatalogCardProvider` / `FakeCollectionPoolProvider` ; extension des tests d’export public ; version `0.4.0`, `README` / `CHANGELOG` / journal mis à jour ; `flake8` `per-file-ignores` pour `pool/__init__.py`.

### Buts

- Livrer la feature **04_pool_protocols_and_providers** : abstraction pool pour génération et validation, sans couplage à une implémentation catalogue ou collection concrète.

### Impact

- Les stratégies de génération et les validateurs pourront interroger un pool typé (disponibilité par nom Oracle) en injectant des adaptateurs respectant les protocoles.

## 2026-04-06 (feature/format-validation)

### Modifications

- Ajout du paquet `validation/` : `FormatDefinition` (orchestration `validate`), `ConstructedFormatDefinition` / `LimitedFormatDefinition`, `DeckConstraint` + `DeckConstraintSet`, `DeckValidationRule` (ABC) et règles concrètes (taille du main, exemplaires max hors bases, taille du sideboard construit, minimum limité, infos/avertissements sideboard limité).
- `DeckValidationIssue` + `DeckValidationIssueSeverity` + `DeckValidationReport` (tri déterministe, `is_valid`, compteurs par gravité).
- Constante `DEFAULT_BASIC_LAND_ORACLE_NAMES` pour la règle des 4 exemplaires.
- Paramètres de format invalides → `DeckConfigurationException`.
- Tests miroir + double partagé `always_error_validation_rule.py` (import `tests.…`), extension des exports publics ; version `0.3.0`, `README` / `CHANGELOG` / journal mis à jour ; `flake8` `per-file-ignores` pour `validation/__init__.py`.
- Fonction partagée `maindeck_minimum_support.issues_when_main_below_minimum` pour éviter la duplication pylint entre règles main min construit / limité ; `[tool.pylint.SIMILARITIES] min-similarity-lines = 10` en complément.

### Buts

- Livrer la feature **03_format_constraints_and_validation** : rapport typé (erreurs, warnings, infos), suggestions et entités affectées, sans dépendance externe.

### Impact

- Les pipelines d’optimisation et d’UI pourront consommer un rapport stable ; les listes de bases / seuils restent extensibles pour Commander, Brawl, etc.

## 2026-04-06 (feature/core-deck-model)

### Modifications

- Ajout du paquet `deck/` : `DeckCardEntry` (nom anglais Oracle + quantité), `DeckSection` (identifiant + entrées, fabriques `main` / `sideboard`), `Deck` (validation des identifiants de sections, totaux, `list_view`, `summary`), `DeckListView` (tri déterministe), `DeckSummary` (totaux, regroupements par nom anglais, cartes `MappingProxyType`).
- Validation métier via `DeckValidationException` (nom vide, quantité invalide, mauvais couple main/sideboard).
- Tests miroir sous `tests/baobab_mtg_deckbuilder/deck/`, extension des tests d’export public.
- Version `0.2.0`, `README` et `CHANGELOG` mis à jour.

### Buts

- Livrer la feature **02_core_deck_model** : représentation propre Construit/Limité, API typée, agrégats sans dépendance externe.

### Impact

- Les features validation de format, génération et optimisation peuvent s’appuyer sur un deck immuable et des synthèses stables (clé de comptage = nom anglais Oracle).

### Suivi

- Réintégration de `.github/workflows/ci.yml` sur `main` (fichier absent après merge de la PR ; workflow CI rétabli pour les push/PR).

## 2026-04-06 (feature/project-bootstrap)

### Modifications

- Création du socle paquet `src/baobab_mtg_deckbuilder/` avec `py.typed` et export public (`__version__`, exceptions).
- Ajout du module `exceptions/` avec une classe par fichier : `BaobabMtgDeckbuilderException`, `DeckValidationException`, `DeckGenerationException`, `DeckOptimizationException`, `DeckSimulationException`, `DeckConfigurationException`.
- Configuration centralisée dans `pyproject.toml` : métadonnées du projet, extras `dev`, black, flake8 (via `Flake8-pyproject`), mypy strict + assouplissements pour `tests.*`, pylint, bandit, pytest-cov avec rapports vers `docs/tests/coverage/`, coverage `fail_under` à 90 %.
- Tests miroir : imports publics, comportement des exceptions, garde-fous sur la présence des options pytest/coverage dans `pyproject.toml`.
- Documentation : `README.md`, `CHANGELOG.md` (0.1.0), `LICENSE`, `docs/tests/coverage/README.md`.
- Workflows GitHub Actions : CI sur push/PR (qualité + tests), release sur tags `v*.*.*` (vérification ancêtre de `main`, build, publication des artefacts). Emplacement correct : `.github/workflows/` (remplace l’ancien dossier `workflow` non reconnu par GitHub).
- Flake8 : `per-file-ignores` pour `src/baobab_mtg_deckbuilder/__init__.py` (ré-exports publics sans faux positifs F401).

### Buts

- Livrer la feature **01_project_bootstrap** : packaging installable en éditable, wheel-ready, outillage qualité unifié, exceptions projet typées et documentées, base documentaire minimale.

### Impact

- Les développements ultérieurs (modèle de deck, validation de format, optimisation, simulation) peuvent s’appuyer sur une hiérarchie d’erreurs stable et sur des garde-fous CI/local identiques.
- La couverture et les rapports sont localisés sous `docs/tests/coverage`, conformément aux contraintes du dépôt.
