# Feature 10 — Optimisation itérative

## Identité

- **Code** : `10_optimization_engine`
- **Branche recommandée** : `feature/optimization-engine`
- **Dépendances** : 01_project_bootstrap, 07_weighted_scoring_and_explanations, 08_generation_strategies, 09_mutation_operators

## Objectif

Implémenter le moteur d’optimisation itérative capable de partir d’un deck ou d’un ensemble de candidats, de générer des variantes, d’évaluer, de conserver les meilleures et de s’arrêter selon des critères explicites.

## Livrables attendus

- Domaine `optimization`
- Stratégies hill climbing, iterative improvement et beam search simple
- Critères d’arrêt configurables
- Historique d’itérations et meilleur candidat conservé

## Classes / objets attendus

- `DeckOptimizationRequest`
- `DeckOptimizationResult`
- `DeckOptimizationIteration`
- `DeckOptimizationStrategy`
- `DeckSearchState`
- `HillClimbingOptimizationStrategy`
- `IterativeImprovementStrategy`
- `BeamSearchOptimizationStrategy`

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

- Optimisation à partir d’un deck initial
- Arrêt sur itérations max
- Arrêt sur stagnation
- Amélioration mesurable d’un cas simple
- Reproductibilité avec seed

## Critères d’acceptation

- L’optimiseur améliore au moins des cas simples et contrôlés
- Les itérations sont historisées
- Les critères d’arrêt fonctionnent et sont testés

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
