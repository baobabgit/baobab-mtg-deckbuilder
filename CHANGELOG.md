# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-04-06

### Added

- Sous-domaine `validation/` : formats `ConstructedFormatDefinition` et `LimitedFormatDefinition`, contraintes (`DeckConstraint`, `DeckConstraintSet`), règles (`DeckValidationRule` et implémentations MVP), issues (`DeckValidationIssue`, `DeckValidationIssueSeverity`) et `DeckValidationReport`.
- Règles MVP Construit : main ≥ 60, ≤ 4 exemplaires par carte hors terrains de base (Oracle anglais, liste `DEFAULT_BASIC_LAND_ORACLE_NAMES`), sideboard ≤ 15.
- Règles MVP Limité : main ≥ 40, info si sideboard non vide, avertissement si sideboard > 15 (repère souple).
- `DeckConfigurationException` si paramètres de format incohérents.
- Export public des symboles validation depuis le package racine.

## [0.2.0] - 2026-04-06

### Added

- Modèle métier `deck` : `Deck`, `DeckCardEntry`, `DeckSection`, `DeckListView`, `DeckSummary` (objets immuables, main + sideboard, agrégats par nom anglais Oracle).
- Constantes `MAIN_DECK_SECTION_ID` et `SIDEBOARD_SECTION_ID` pour identifier les sections standard (Construit / Limité).
- Export public des types deck depuis le package racine.

## [0.1.0] - 2026-04-06

### Added

- Structure de paquet `src/baobab_mtg_deckbuilder` et tests miroir sous `tests/`.
- `pyproject.toml` avec packaging setuptools, extras `dev`, et configuration black, pylint, mypy, flake8, bandit, pytest et coverage (seuil 90 %, rapports sous `docs/tests/coverage`).
- Hiérarchie d’exceptions projet : `BaobabMtgDeckbuilderException` et sous-classes validation, génération, optimisation, simulation, configuration.
- Export public minimal via `baobab_mtg_deckbuilder.__init__` (`__version__`, exceptions).
- Documentation de base : `README.md`, `CHANGELOG.md`, `docs/dev_diary.md`, `docs/tests/coverage/README.md`.
- Licence MIT.
- CI GitHub Actions (`.github/workflows/ci.yml`) et release sur tag (`.github/workflows/release.yml`).
