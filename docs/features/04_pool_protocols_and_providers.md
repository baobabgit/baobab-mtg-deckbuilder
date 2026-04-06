# Feature 04 — Pool de cartes et protocoles d’accès externes

## Identité

- **Code** : `04_pool_protocols_and_providers`
- **Branche recommandée** : `feature/pool-protocols`
- **Dépendances** : 01_project_bootstrap, 02_core_deck_model, 03_format_constraints_and_validation

## Objectif

Créer l’abstraction de pool et les protocoles d’accès au catalogue et à la collection, sans couplage fort avec les autres briques de l’écosystème.

## Livrables attendus

- Domaine `pool` complet
- Représentation du pool théorique et réel
- Protocoles structuraux vers catalogue et collection
- Interfaces suffisamment riches pour la génération et la validation

## Classes / objets attendus

- `CardPool`
- `CardPoolEntry`
- `CatalogCardProviderProtocol`
- `CollectionPoolProviderProtocol`

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

- Construction d’un pool
- Interrogation des quantités disponibles
- Tests avec providers factices

## Critères d’acceptation

- Aucun couplage à une implémentation concrète externe
- Les protocoles sont strictement typés
- Le pool est exploitable par les stratégies de génération

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
