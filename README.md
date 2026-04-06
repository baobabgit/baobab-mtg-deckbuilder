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
