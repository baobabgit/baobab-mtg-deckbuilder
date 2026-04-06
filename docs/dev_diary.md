# Journal de développement

Les entrées les plus récentes apparaissent en premier.

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
