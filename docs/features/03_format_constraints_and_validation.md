# Feature 03 — Formats, contraintes et validation structurelle

## Identité

- **Code** : `03_format_constraints_and_validation`
- **Branche recommandée** : `feature/format-validation`
- **Dépendances** : 01_project_bootstrap, 02_core_deck_model

## Objectif

Créer le sous-domaine des formats et des règles de validation pour Construit et Limité, avec rapport détaillé d’erreurs, avertissements et informations.

## Livrables attendus

- Définitions de formats `ConstructedFormatDefinition` et `LimitedFormatDefinition`
- Système de contraintes et règles de validation
- Rapport détaillé de validation avec issues typées
- Support des règles MVP : 60+ cartes / 4 exemplaires max hors terrains de base / sideboard <=15 en Construit, 40+ cartes en Limité

## Classes / objets attendus

- `DeckConstraint`
- `DeckConstraintSet`
- `FormatDefinition`
- `ConstructedFormatDefinition`
- `LimitedFormatDefinition`
- `DeckValidationRule`
- `DeckValidationIssue`
- `DeckValidationReport`

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

- Deck Construit valide
- Deck Construit invalide par taille
- Deck Construit invalide par nombre d’exemplaires
- Deck Construit invalide par sideboard
- Deck Limité valide et invalide

## Critères d’acceptation

- Le rapport de validation distingue erreurs, warnings et infos
- Les règles MVP sont couvertes par des tests
- Les objets concernés et propositions de correction peuvent être renseignés

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
