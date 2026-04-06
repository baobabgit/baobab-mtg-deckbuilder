# Feature 12 — Adaptateur de simulation, intégration factice et API publique

## Identité

- **Code** : `12_simulation_adapter_and_public_api`
- **Branche recommandée** : `feature/simulation-api`
- **Dépendances** : 01_project_bootstrap, 08_generation_strategies, 10_optimization_engine, 11_comparison_and_ranking

## Objectif

Préparer l’intégration au rules engine via protocole, fournir un adaptateur factice testable, stabiliser l’API publique et compléter la documentation d’usage.

## Livrables attendus

- Domaine `simulation`
- Protocoles et objets de requête/résultat de simulation
- Fake adapter pour tests d’intégration légers
- Squelette d’adaptateur rules engine sans couplage dur
- API publique claire via `__init__.py` et exemples d’usage

## Classes / objets attendus

- `DeckSimulationAdapterProtocol`
- `DeckSimulationRequest`
- `DeckSimulationResult`
- `MatchupResult`
- `FakeSimulationAdapter`
- `RulesEngineSimulationAdapter`

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

- Tests d’intégration légers avec fake adapter
- Appels via protocole
- Stabilité de l’API publique
- Exemples d’usage exécutables si possible

## Critères d’acceptation

- Le deckbuilder fonctionne sans simulation réelle
- Le fake adapter permet les tests d’intégration
- Le branchement vers un rules engine réel est préparé sans couplage
- L’API publique est stable, concise et documentée

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
