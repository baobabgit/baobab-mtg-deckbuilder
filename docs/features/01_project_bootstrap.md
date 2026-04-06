# Feature 01 — Project bootstrap, packaging et socle qualité

## Identité

- **Code** : `01_project_bootstrap`
- **Branche recommandée** : `feature/project-bootstrap`
- **Dépendances** : Aucune

## Objectif

Mettre en place la structure initiale de la librairie, le packaging, la configuration centralisée des outils, la hiérarchie d’exceptions projet et la base documentaire minimale.

## Livrables attendus

- Structure `src/baobab_mtg_deckbuilder/` et `tests/` conforme aux contraintes
- `pyproject.toml` complet avec configuration `black`, `pylint`, `mypy`, `flake8`, `bandit`, `pytest`, `coverage`
- Hiérarchie d’exceptions projet minimale
- `README.md`, `CHANGELOG.md`, `docs/dev_diary.md`, couverture dans `docs/tests/coverage`
- Export public minimal via `__init__.py`

## Classes / objets attendus

- `BaobabMtgDeckbuilderException`
- `DeckValidationException`
- `DeckGenerationException`
- `DeckOptimizationException`
- `DeckSimulationException`
- `DeckConfigurationException`

## Périmètre détaillé

Cette feature doit être développée comme un incrément cohérent, autonome et testable.
Elle doit produire une valeur métier immédiate tout en préparant les extensions futures prévues
par le projet (`Commander`, `Brawl`, simulation réelle, self-play, optimisation avancée).

### Attendus fonctionnels

- Implémenter uniquement ce qui relève directement de la feature.
- Concevoir les points d’extension nécessaires sans surdévelopper les futures fonctionnalités.
- Exposer des objets métier typés, explicites et documentés.
- Garantir un comportement déterministe dès qu’un seed ou un paramètre de configuration l’impose.
- Préserver l’explicabilité des sorties.

### Hors périmètre

- Exposition HTTP
- Interface utilisateur
- Couplage dur au front
- Couplage dur à une implémentation concrète de `baobab-mtg-rules-engine`
- Logique de collection physique ou produit scellé

## Exigences techniques

- Une classe par fichier.
- Arborescence miroir entre `src/` et `tests/`.
- Typage complet et compatible `mypy --strict`.
- Docstrings reStructuredText sur toutes les API publiques.
- Exceptions projet dédiées pour toute erreur métier spécifique.
- Configuration et outillage centralisés dans `pyproject.toml`.

## Tests à produire

- Tests de base sur l’import de la librairie
- Tests des exceptions projet
- Vérification de la configuration pytest/coverage

## Critères d’acceptation

- Le projet est installable en mode editable et wheel-ready
- Tous les outils qualité passent
- La base documentaire est présente
- Les exceptions projet sont définies et typées

## Définition de terminé

La feature est terminée lorsque :
- le code est implémenté ;
- les tests unitaires associés existent et passent ;
- la couverture reste conforme ;
- les outils qualité passent ;
- la documentation utile est mise à jour ;
- `docs/dev_diary.md` est mis à jour ;
- la Pull Request est prête puis mergée sur `main` après validation.

## Notes d’implémentation

- Favoriser les objets métier plutôt que les dictionnaires libres.
- Éviter toute hypothèse cachée ; documenter les constantes métier importantes.
- Préparer les extensions futures sans les implémenter prématurément.
