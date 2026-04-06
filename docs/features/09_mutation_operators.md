# Feature 09 — Mutations et variantes de deck

## Identité

- **Code** : `09_mutation_operators`
- **Branche recommandée** : `feature/mutation-operators`
- **Dépendances** : 01_project_bootstrap, 02_core_deck_model, 04_pool_protocols_and_providers, 07_weighted_scoring_and_explanations, 08_generation_strategies

## Objectif

Créer le système de mutations traçables pour faire évoluer un deck existant par transformations contrôlées et explicables.

## Livrables attendus

- Domaine `mutation`
- Opérateurs de remplacement de carte, ajustement de terrains, correction de couleur et échange de rôle
- Traçabilité avant/après
- Résultats de mutation structurés

## Classes / objets attendus

- `DeckMutation`
- `DeckMutationOperator`
- `DeckMutationResult`
- `DeckReplacementSuggestion`
- `ReplaceCardOperator`
- `AdjustLandCountOperator`
- `ColorFixOperator`
- `RoleSwapOperator`

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

- Mutation bénéfique
- Mutation neutre
- Mutation dégradante
- Traçabilité des changements
- Compatibilité avec validation

## Critères d’acceptation

- Chaque mutation est explicable et testée
- Le résultat contient avant/après et justification
- Les mutations peuvent être chaînées par l’optimiseur

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
