# Feature 11 — Comparaison, ranking et recommandation

## Identité

- **Code** : `11_comparison_and_ranking`
- **Branche recommandée** : `feature/comparison-ranking`
- **Dépendances** : 01_project_bootstrap, 07_weighted_scoring_and_explanations, 10_optimization_engine

## Objectif

Permettre la comparaison structurée de plusieurs decks, la production d’un classement et l’explication des écarts.

## Livrables attendus

- Domaine `comparison`
- Classement multi-critères
- Rapport de comparaison lisible
- Justification de la recommandation finale

## Classes / objets attendus

- `DeckComparison`
- `DeckRanking`
- `DeckComparisonCriterion`
- `DeckComparisonReport`

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

- Classement de plusieurs decks
- Comparaison sur score global et sous-scores
- Rapport explicatif cohérent

## Critères d’acceptation

- Le système sait ordonner plusieurs decks sur des cas contrôlés
- Le rapport explique clairement pourquoi un deck est devant un autre
- Les résultats sont réutilisables par l’API publique

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
