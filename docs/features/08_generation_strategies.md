# Feature 08 — Génération de decks candidats

## Identité

- **Code** : `08_generation_strategies`
- **Branche recommandée** : `feature/generation-strategies`
- **Dépendances** : 01_project_bootstrap, 03_format_constraints_and_validation, 04_pool_protocols_and_providers, 07_weighted_scoring_and_explanations

## Objectif

Implémenter les requêtes de génération, les résultats et les premières stratégies de construction de decks candidats à partir d’un pool.

## Livrables attendus

- Domaine `generation`
- Stratégies random seedée, gloutonne, guidée par contraintes et hybride simple
- Support des seeds pour reproductibilité
- Résultats structurés avec candidats multiples

## Classes / objets attendus

- `DeckGenerationRequest`
- `DeckGenerationResult`
- `DeckCandidate`
- `DeckGenerationStrategy`
- `RandomSeededGenerationStrategy`
- `GreedyGenerationStrategy`
- `ConstrainedGenerationStrategy`
- `HybridGenerationStrategy`

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

- Génération de plusieurs decks valides
- Reproductibilité à seed identique
- Respect du format et du pool
- Comparaison basique entre stratégies

## Critères d’acceptation

- Au moins une stratégie produit systématiquement des decks valides quand le pool le permet
- Les stratégies restent déterministes avec seed fixe
- Les résultats sont typés et documentés

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
