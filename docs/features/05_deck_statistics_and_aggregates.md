# Feature 05 — Statistiques de deck et agrégats analytiques

## Identité

- **Code** : `05_deck_statistics_and_aggregates`
- **Branche recommandée** : `feature/deck-statistics`
- **Dépendances** : 01_project_bootstrap, 02_core_deck_model, 04_pool_protocols_and_providers

## Objectif

Fournir les calculs analytiques de base utilisés par la validation, l’évaluation et l’explicabilité : courbe de mana, répartition par couleur, par type, terrains, coûts et copies.

## Livrables attendus

- Module utilitaire de statistiques
- Calculs réutilisables et testables indépendamment
- Agrégats cohérents avec le modèle métier

## Classes / objets attendus

- `DeckStatistics`

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

- Courbe de mana sur cas simples
- Répartition par couleur
- Répartition par type
- Nombre de terrains
- Copies par nom anglais

## Critères d’acceptation

- Les statistiques sont découplées des stratégies
- Les résultats sont déterministes et documentés
- Les cas d’absence d’information sont gérés proprement

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
