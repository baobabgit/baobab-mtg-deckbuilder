# Feature 02 — Modèle métier du deck

## Identité

- **Code** : `02_core_deck_model`
- **Branche recommandée** : `feature/core-deck-model`
- **Dépendances** : 01_project_bootstrap

## Objectif

Implémenter les objets métier centraux représentant un deck, ses entrées, ses sections, ses vues et ses synthèses, avec un modèle immuable ou au minimum fortement maîtrisé.

## Livrables attendus

- Objets du domaine `deck`
- Gestion du main deck et du sideboard
- Agrégats de base : taille totale, quantités, regroupements
- Support du nom anglais comme clé de comptage métier

## Classes / objets attendus

- `Deck`
- `DeckCardEntry`
- `DeckSection`
- `DeckListView`
- `DeckSummary`

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

- Création de deck valide
- Calcul de taille et quantités
- Comptage par nom anglais
- Gestion des sections et sideboard

## Critères d’acceptation

- Le modèle de deck permet de représenter proprement Construit et Limité
- Les objets exposent une API typée et documentée
- Les agrégats de base sont disponibles sans dépendance externe

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
