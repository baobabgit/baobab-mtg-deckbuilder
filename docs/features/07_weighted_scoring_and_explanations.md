# Feature 07 — Score agrégé et explainability

## Identité

- **Code** : `07_weighted_scoring_and_explanations`
- **Branche recommandée** : `feature/weighted-scoring`
- **Dépendances** : 01_project_bootstrap, 06_heuristic_evaluation_metrics

## Objectif

Assembler les métriques en évaluation globale, avec poids configurables, breakdown détaillé, pénalités/bonus et explications exploitables.

## Livrables attendus

- Objets `DeckScore`, `DeckEvaluation`, `DeckEvaluationBreakdown`
- Agrégateur pondéré
- Configuration des poids par défaut
- Explication complète de la composition du score

## Classes / objets attendus

- `DeckScore`
- `DeckEvaluation`
- `DeckEvaluationBreakdown`
- `WeightedScoreAggregator`

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

- Agrégation pondérée sur cas contrôlés
- Application de pénalités et bonus
- Stabilité du breakdown
- Lisibilité des explications

## Critères d’acceptation

- Le score global n’est jamais opaque
- La configuration des poids est sérialisable et documentée
- Le breakdown permet d’expliquer un classement ou une recommandation

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
