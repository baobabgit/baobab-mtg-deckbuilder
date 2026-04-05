# Cahier des charges — `baobab-mtg-deckbuilder`

## 1. Objet du document

Ce document définit le cahier des charges complet de la librairie Python `baobab-mtg-deckbuilder`.

La librairie a pour responsabilité de construire, évaluer, comparer et améliorer automatiquement des decks **Magic: The Gathering** à partir :
- d’un pool de cartes,
- d’une collection réelle,
- d’un format cible,
- de contraintes métier,
- d’objectifs d’optimisation explicites.

Elle constitue la brique d’intelligence de construction de deck de l’écosystème Baobab MTG.

---

## 2. Vision produit

`baobab-mtg-deckbuilder` doit permettre de transformer un ensemble de cartes disponibles en listes de decks **valides, explicables, comparables et optimisables**.

La librairie doit :
- séparer clairement la **construction**, la **validation**, l’**évaluation** et l’**optimisation** ;
- être **testable sans simulation lourde** ;
- permettre un **branchement progressif** vers le moteur de règles ;
- exposer des résultats **interprétables**, et non un score opaque ;
- rester une **librairie métier** pure, sans responsabilité d’API web ni d’interface graphique.

---

## 3. Positionnement dans l’architecture

## 3.1 Rôle

La librairie est une brique métier de haut niveau, dédiée à l’optimisation de decks.

## 3.2 Dépendances autorisées

La librairie peut dépendre de :
- `baobab-mtg-catalog` pour la connaissance des cartes ;
- `baobab-mtg-rules-engine` pour l’évaluation par simulation ;
- `baobab-probability-core` pour les calculs probabilistes ;
- une brique de collection, **via interface / protocole**, pour le pool réellement disponible.

## 3.3 Dépendances interdites

La librairie ne doit pas dépendre :
- ni d’une API web,
- ni d’un front,
- ni d’une logique de produit scellé,
- ni de la gestion physique de collection,
- ni du scan de codes-barres.

---

## 4. Objectifs métier

## 4.1 Objectifs principaux

La librairie doit permettre de :
1. représenter un deck et ses variantes ;
2. valider un deck selon un format et des contraintes données ;
3. construire un ou plusieurs decks à partir d’un pool ;
4. attribuer un score détaillé à un deck ;
5. générer des mutations et variantes ;
6. comparer plusieurs listes ;
7. optimiser itérativement un deck ;
8. préparer des campagnes de self-play via le moteur de règles.

## 4.2 Objectifs secondaires

La librairie doit également :
- rendre les résultats reproductibles ;
- permettre la configuration fine des poids de scoring ;
- fournir des explications compréhensibles sur les décisions et scores ;
- permettre une montée en sophistication progressive.

---

## 5. Périmètre fonctionnel

## 5.1 Inclus dans le périmètre

Le projet doit gérer :
- la représentation des decks ;
- les contraintes de construction ;
- les règles de validation de deck ;
- le scoring heuristique ;
- la génération de variantes ;
- la comparaison de decks ;
- la sélection des meilleures listes ;
- l’intégration par abstraction avec le moteur de simulation ;
- l’orchestration d’optimisation locale ou guidée.

## 5.2 Hors périmètre

Le projet ne doit pas gérer :
- les règles détaillées de résolution d’une partie par lui-même ;
- l’exposition HTTP ;
- l’interface utilisateur ;
- la persistance distante ;
- la gestion de collection détaillée ;
- la gestion du catalogue complet à lui seul ;
- les produits scellés ;
- les scans ou EAN/barcodes.

---

## 6. Cadrage de version

## 6.1 Priorité de la première version exploitable

La première version exploitable doit prioriser :
- le **Construit** ;
- le **Limité** ;
- des heuristiques de scoring explicables ;
- des stratégies de génération déterministes et testables ;
- une intégration **optionnelle** au moteur de règles via interface.

## 6.2 Extensions prévues mais non obligatoires en première livraison

Sont prévues comme extensions progressives :
- Commander ;
- Brawl ;
- simulation réelle à grande échelle ;
- self-play complet IA contre IA ;
- stratégies méta-dépendantes ou adaptatives.

---

## 7. Règles métier MTG à prendre en compte

## 7.1 Construit

Le système de validation doit permettre de couvrir au minimum :
- deck de **60 cartes minimum** ;
- **4 exemplaires maximum** par carte non terrain de base ;
- sideboard de **15 cartes maximum** ;
- calcul du nombre d’exemplaires sur le **nom anglais** de la carte.

## 7.2 Limité

Le système de validation doit permettre de couvrir au minimum :
- deck de **40 cartes minimum** ;
- nombre d’exemplaires dépendant du pool réellement disponible.

## 7.3 Commander et Brawl

Ces formats doivent être prévus dans l’architecture, mais peuvent être livrés après le socle Construit / Limité.

Le modèle doit néanmoins être conçu pour supporter ensuite :
- identité couleur ;
- singleton hors terrains de base ;
- deck de 100 cartes en Commander ;
- deck de 60 cartes en Brawl ;
- commandant explicite ;
- contraintes spécifiques de format.

---

## 8. Cas d’usage cibles

La librairie doit couvrir au minimum les cas d’usage suivants :

1. Construire un deck valide à partir d’un pool donné.
2. Construire plusieurs propositions de decks compatibles avec un format.
3. Évaluer un deck selon des heuristiques simples.
4. Comparer plusieurs decks sur la base d’un score détaillé.
5. Améliorer un deck existant par mutations successives.
6. Lancer une optimisation guidée par objectifs.
7. Préparer une campagne de simulation contre un panel de decks de référence.
8. Renvoyer des explications compréhensibles sur les raisons d’un score ou d’un rejet.

---

## 9. Architecture fonctionnelle attendue

La librairie doit être organisée en sous-domaines explicites.

## 9.1 Domaine `deck`

Responsabilités :
- représenter un deck ;
- représenter son sideboard ;
- représenter les sections éventuelles ;
- fournir des vues et agrégats utiles.

Objets attendus :
- `Deck`
- `DeckCardEntry`
- `DeckSection`
- `DeckListView`
- `DeckSummary`

## 9.2 Domaine `constraints`

Responsabilités :
- représenter les contraintes applicables ;
- agréger des règles ;
- paramétrer les formats.

Objets attendus :
- `DeckConstraintSet`
- `DeckConstraint`
- `FormatDefinition`
- `DeckValidationRule`
- `DeckValidationReport`
- `DeckValidationIssue`

## 9.3 Domaine `pool`

Responsabilités :
- représenter le pool disponible ;
- distinguer pool théorique et pool réel ;
- exposer un accès uniforme aux cartes disponibles.

Objets attendus :
- `CardPool`
- `CardPoolEntry`
- `CollectionPoolProviderProtocol`
- `CatalogCardProviderProtocol`

## 9.4 Domaine `evaluation`

Responsabilités :
- calculer des métriques ;
- produire un score détaillé ;
- fournir des explications.

Objets attendus :
- `DeckEvaluation`
- `DeckScore`
- `DeckMetric`
- `DeckEvaluationBreakdown`
- `DeckEvaluationExplanation`

## 9.5 Domaine `generation`

Responsabilités :
- construire des listes candidates ;
- appliquer des stratégies de sélection ;
- produire plusieurs decks.

Objets attendus :
- `DeckGenerationRequest`
- `DeckGenerationStrategy`
- `DeckGenerationResult`
- `DeckCandidate`

## 9.6 Domaine `mutation`

Responsabilités :
- créer des variantes d’un deck ;
- appliquer des transformations contrôlées ;
- tracer les changements.

Objets attendus :
- `DeckMutation`
- `DeckMutationOperator`
- `DeckMutationResult`
- `DeckReplacementSuggestion`

## 9.7 Domaine `optimization`

Responsabilités :
- piloter les itérations ;
- conserver les meilleurs candidats ;
- appliquer des stratégies de recherche.

Objets attendus :
- `DeckOptimizationRequest`
- `DeckOptimizationStrategy`
- `DeckOptimizationIteration`
- `DeckOptimizationResult`
- `DeckSearchState`

## 9.8 Domaine `simulation`

Responsabilités :
- intégrer le moteur de règles via abstraction ;
- permettre des évaluations simulées sans couplage dur.

Objets attendus :
- `DeckSimulationAdapterProtocol`
- `DeckSimulationRequest`
- `DeckSimulationResult`
- `MatchupResult`

## 9.9 Domaine `comparison`

Responsabilités :
- comparer plusieurs decks ;
- produire des classements ;
- expliquer les écarts.

Objets attendus :
- `DeckComparison`
- `DeckRanking`
- `DeckComparisonCriterion`
- `DeckComparisonReport`

---

## 10. Exigences fonctionnelles détaillées

## 10.1 Représentation de deck

Le système doit permettre :
- de représenter un deck principal ;
- de représenter un sideboard ;
- d’associer une quantité à chaque carte ;
- d’obtenir des agrégats :
  - taille totale,
  - courbe de mana,
  - répartition par couleur,
  - répartition par type,
  - nombre de terrains,
  - nombre de copies par nom anglais.

## 10.2 Validation

Le système doit :
- valider un deck selon un format explicite ;
- renvoyer un rapport détaillé ;
- distinguer :
  - erreurs bloquantes,
  - avertissements,
  - informations.

Le rapport doit au minimum préciser :
- contrainte vérifiée ;
- statut ;
- détail ;
- objets concernés ;
- proposition éventuelle de correction.

## 10.3 Définition de format

Un format doit pouvoir définir :
- taille minimale ou exacte du deck ;
- taille maximale du sideboard ;
- nombre maximal d’exemplaires ;
- règles spécifiques de couleur ;
- règles spécifiques de commandant ;
- règles d’éligibilité des cartes ;
- règles spécifiques de version future.

Le système doit fournir au minimum :
- `ConstructedFormatDefinition`
- `LimitedFormatDefinition`

Le design doit permettre d’ajouter ensuite :
- `CommanderFormatDefinition`
- `BrawlFormatDefinition`

## 10.4 Évaluation heuristique

La librairie doit fournir une évaluation heuristique sans dépendre du moteur de règles.

Les premières métriques minimales attendues sont :
- qualité de la courbe de mana ;
- équilibre du nombre de terrains ;
- cohérence des couleurs ;
- adéquation coût / base de mana ;
- équilibre des types de cartes ;
- cohérence avec un plan de jeu simple ;
- respect des contraintes de format.

Chaque métrique doit :
- être nommée ;
- être indépendante ;
- avoir un poids configurable ;
- produire un score brut ;
- produire un score normalisé ;
- produire une explication textuelle.

## 10.5 Score agrégé

Le système doit calculer un score global à partir :
- de métriques détaillées ;
- de poids configurables ;
- d’éventuelles pénalités ;
- d’éventuels bonus.

Le score global ne doit jamais être opaque.
Il doit toujours être possible d’expliquer :
- la composition du score ;
- les pénalités appliquées ;
- les hypothèses retenues.

## 10.6 Génération de deck

La librairie doit permettre de générer un ou plusieurs decks à partir :
- d’un pool de cartes ;
- d’un format ;
- d’une stratégie ;
- de contraintes supplémentaires ;
- d’un objectif d’optimisation.

La génération doit supporter au minimum :
- une stratégie de génération aléatoire contrôlée ;
- une stratégie guidée par contraintes ;
- une stratégie gloutonne simple ;
- une stratégie hybride heuristique.

## 10.7 Mutation

La librairie doit permettre de produire des variantes en appliquant des mutations typées, par exemple :
- remplacement d’une carte par une autre ;
- ajustement du nombre de terrains ;
- substitution de cartes d’un même rôle ;
- correction de couleur ;
- ajustement de courbe ;
- modification ciblée du sideboard.

Chaque mutation doit être :
- traçable ;
- réversible conceptuellement ;
- explicable ;
- évaluée avant et après application.

## 10.8 Optimisation

La librairie doit fournir un moteur d’optimisation itératif capable de :
- partir d’un deck initial ou d’un ensemble de candidats ;
- générer des variantes ;
- évaluer les variantes ;
- conserver les meilleures ;
- stopper selon des critères explicites.

Critères d’arrêt attendus :
- nombre maximal d’itérations ;
- stagnation du score ;
- budget temps ;
- nombre maximal d’évaluations ;
- objectif atteint.

## 10.9 Comparaison

Le système doit comparer plusieurs decks selon :
- score global ;
- sous-scores ;
- conformité ;
- stabilité ;
- résultats simulés quand disponibles.

Le résultat doit permettre :
- un classement ;
- une justification ;
- des recommandations de choix.

## 10.10 Intégration simulation

Le moteur de deckbuilding ne doit pas connaître l’implémentation interne du moteur de règles.

L’intégration doit se faire par protocole/interface.

Le système doit permettre :
- l’absence totale de simulation ;
- l’usage d’un adaptateur factice pour les tests ;
- l’usage ultérieur d’un adaptateur réel vers `baobab-mtg-rules-engine`.

## 10.11 Reproductibilité

Toute génération non triviale doit pouvoir être reproduite via :
- un seed explicite ;
- des paramètres d’exécution sérialisables ;
- un historique des mutations ou décisions structurantes.

## 10.12 Explainability

Le système doit produire des sorties explicables à tous les niveaux :
- pourquoi un deck est invalide ;
- pourquoi un deck est mieux classé ;
- pourquoi une mutation a été retenue ;
- pourquoi une carte a été proposée ou retirée ;
- quelles métriques ont fait évoluer le score.

---

## 11. Contraintes de conception

## 11.1 Découplage fort

Le projet doit séparer strictement :
- le modèle métier ;
- les règles de validation ;
- l’évaluation ;
- la génération ;
- l’optimisation ;
- les adaptateurs externes.

## 11.2 Dépendance par protocoles

Les accès au catalogue, à la collection et à la simulation doivent passer par des protocoles ou interfaces structurales.

## 11.3 Pas de connaissance implicite

Les comportements ne doivent pas dépendre de constantes cachées.
Toute hypothèse métier importante doit être configurable ou clairement documentée.

## 11.4 Déterminisme

À paramètres et seed identiques, les résultats doivent être identiques.

## 11.5 Sorties structurées

Les résultats doivent être des objets métier explicites, pas des dictionnaires libres non typés.

---

## 12. Proposition d’arborescence

```text
src/baobab_mtg_deckbuilder/
├── __init__.py
├── constants/
│   └── scoring_defaults.py
├── exceptions/
│   ├── __init__.py
│   ├── base_exception.py
│   ├── validation_exception.py
│   ├── generation_exception.py
│   ├── optimization_exception.py
│   └── simulation_exception.py
├── deck/
│   ├── deck.py
│   ├── deck_card_entry.py
│   ├── deck_section.py
│   ├── deck_summary.py
│   └── deck_list_view.py
├── constraints/
│   ├── deck_constraint.py
│   ├── deck_constraint_set.py
│   ├── format_definition.py
│   ├── constructed_format_definition.py
│   ├── limited_format_definition.py
│   ├── deck_validation_rule.py
│   ├── deck_validation_issue.py
│   └── deck_validation_report.py
├── pool/
│   ├── card_pool.py
│   ├── card_pool_entry.py
│   ├── catalog_card_provider_protocol.py
│   └── collection_pool_provider_protocol.py
├── evaluation/
│   ├── deck_evaluation.py
│   ├── deck_score.py
│   ├── deck_metric.py
│   ├── deck_evaluation_breakdown.py
│   ├── deck_evaluation_explanation.py
│   ├── evaluators/
│   │   ├── mana_curve_evaluator.py
│   │   ├── land_ratio_evaluator.py
│   │   ├── color_balance_evaluator.py
│   │   ├── mana_base_consistency_evaluator.py
│   │   └── card_type_balance_evaluator.py
│   └── aggregators/
│       └── weighted_score_aggregator.py
├── generation/
│   ├── deck_generation_request.py
│   ├── deck_generation_result.py
│   ├── deck_candidate.py
│   ├── deck_generation_strategy.py
│   └── strategies/
│       ├── random_seeded_generation_strategy.py
│       ├── greedy_generation_strategy.py
│       ├── constrained_generation_strategy.py
│       └── hybrid_generation_strategy.py
├── mutation/
│   ├── deck_mutation.py
│   ├── deck_mutation_result.py
│   ├── deck_mutation_operator.py
│   └── operators/
│       ├── replace_card_operator.py
│       ├── adjust_land_count_operator.py
│       ├── color_fix_operator.py
│       └── role_swap_operator.py
├── optimization/
│   ├── deck_optimization_request.py
│   ├── deck_optimization_result.py
│   ├── deck_optimization_iteration.py
│   ├── deck_optimization_strategy.py
│   ├── deck_search_state.py
│   └── strategies/
│       ├── hill_climbing_optimization_strategy.py
│       ├── beam_search_optimization_strategy.py
│       └── iterative_improvement_strategy.py
├── comparison/
│   ├── deck_comparison.py
│   ├── deck_ranking.py
│   ├── deck_comparison_criterion.py
│   └── deck_comparison_report.py
├── simulation/
│   ├── deck_simulation_adapter_protocol.py
│   ├── deck_simulation_request.py
│   ├── deck_simulation_result.py
│   └── matchup_result.py
├── adapters/
│   ├── fake/
│   │   └── fake_simulation_adapter.py
│   └── rules_engine/
│       └── rules_engine_simulation_adapter.py
└── utils/
    ├── seed_tools.py
    └── deck_statistics.py
```

---

## 13. Exceptions

Le projet doit définir une hiérarchie d’exceptions dédiée.

Base requise :
- `BaobabMtgDeckbuilderException`

Spécialisations minimales :
- `DeckValidationException`
- `DeckGenerationException`
- `DeckOptimizationException`
- `DeckSimulationException`
- `DeckConfigurationException`

Règle complémentaire :
- toute erreur métier spécifique au projet doit faire l’objet d’une exception spécifique du projet.

---

## 14. Stratégie de développement attendue

## 14.1 Niveau 1 — socle

À livrer en priorité :
- représentation de deck ;
- contraintes de format ;
- validation structurelle ;
- statistiques de deck ;
- heuristiques simples ;
- score détaillé explicable ;
- génération simple ;
- mutations de base.

## 14.2 Niveau 2 — enrichissement

À livrer ensuite :
- score composite configurable ;
- comparaison de decks ;
- optimisation itérative ;
- exploration guidée ;
- stratégies de recherche alternatives.

## 14.3 Niveau 3 — simulation avancée

À livrer ensuite :
- branchement réel au moteur de règles ;
- campagnes de simulation ;
- amélioration par confrontation ;
- self-play progressif.

---

## 15. Exigences de qualité logicielle

Le développement doit respecter strictement les contraintes de développement du projet.

## 15.1 Langage et style

- Python moderne ;
- PEP 8 ;
- code orienté objets ;
- noms explicites ;
- une classe par fichier ;
- arborescence logique.

## 15.2 Typage

- annotations de type obligatoires partout ;
- `mypy` strict ;
- protocoles pour les interfaces structurelles.

## 15.3 Qualité

Le code doit passer sans erreur :
- `black`
- `pylint`
- `mypy`
- `flake8`
- `bandit`

## 15.4 Documentation

Le projet doit inclure :
- `README.md`
- `CHANGELOG.md`
- docstrings reStructuredText sur les classes et méthodes publiques
- `docs/dev_diary.md`

## 15.5 Configuration centralisée

La configuration doit être centralisée dans `pyproject.toml` dès que possible.

## 15.6 Dépendances

- séparation stricte entre dépendances de production et de développement ;
- contraintes de versions explicites ;
- dépendances minimales.

---

## 16. Exigences de tests

## 16.1 Structure

- un fichier de test par classe ;
- structure miroir entre `src/` et `tests/` ;
- classes de tests explicites.

## 16.2 Couverture

- couverture unitaire minimale : **90%** ;
- rapports de couverture dans `docs/tests/coverage`.

## 16.3 Tests attendus

Le projet doit comporter au minimum :
- tests unitaires des modèles ;
- tests unitaires des règles de validation ;
- tests unitaires des évaluateurs ;
- tests unitaires des agrégateurs de score ;
- tests unitaires des stratégies de génération ;
- tests unitaires des opérateurs de mutation ;
- tests unitaires des stratégies d’optimisation ;
- tests d’intégration légers avec un adaptateur de simulation factice ;
- tests de reproductibilité avec seed ;
- tests de non-régression sur exemples de decks.

## 16.4 Jeux de tests minimums

Prévoir au minimum :
- decks construits valides ;
- decks construits invalides ;
- decks limités valides ;
- variations de taille ;
- variations de nombre d’exemplaires ;
- incohérences de couleur ;
- scoring attendu sur cas simples ;
- classement de plusieurs decks ;
- mutation bénéfique, neutre et dégradante.

---

## 17. Exigences de performance

La première version n’a pas besoin d’être massivement distribuée, mais doit respecter :

- temps de validation court sur un deck standard ;
- temps de scoring heuristique faible ;
- optimisation testable localement sur un petit nombre d’itérations ;
- absence d’algorithmes inutilement explosifs dans le MVP.

Des budgets indicatifs peuvent être utilisés :
- validation d’un deck simple : très courte ;
- scoring heuristique d’un deck : très court ;
- optimisation locale sur petit pool : raisonnable pour un usage de développement.

---

## 18. API publique attendue

La librairie doit exposer une API Python claire et stable.

Exemples d’entrées attendues :
- créer un deck depuis une liste d’entrées ;
- valider un deck selon un format ;
- évaluer un deck ;
- générer des decks à partir d’un pool ;
- optimiser un deck existant ;
- comparer plusieurs decks.

L’API publique doit être :
- concise ;
- typée ;
- documentée ;
- stable.

---

## 19. Livrables attendus

Le développement doit produire au minimum :

1. le code source de la librairie ;
2. les tests unitaires et d’intégration légère ;
3. le `pyproject.toml` complet ;
4. le `README.md` ;
5. le `CHANGELOG.md` ;
6. le `docs/dev_diary.md` ;
7. les rapports de couverture dans `docs/tests/coverage` ;
8. une documentation minimale d’usage ;
9. des exemples d’utilisation ;
10. un adaptateur de simulation factice pour tests.

---

## 20. Critères d’acceptation

Le projet sera considéré conforme si :

1. la librairie construit et valide correctement des decks Construit et Limité ;
2. la librairie calcule un score détaillé explicable ;
3. la librairie peut générer plusieurs candidats à partir d’un pool ;
4. la librairie peut muter et améliorer un deck simple ;
5. la librairie peut comparer plusieurs decks ;
6. la librairie supporte une intégration simulation via protocole ;
7. la librairie ne dépend ni d’une API web ni d’un front ;
8. les résultats peuvent être reproduits avec un seed ;
9. toutes les contraintes de développement sont respectées ;
10. la couverture unitaire atteint au moins 90%.

---

## 21. Workflow Git attendu

Le développement doit suivre les contraintes du projet :

- une branche dédiée par fonctionnalité ou correction ;
- nommage explicite de branche ;
- commits au format Conventional Commits ;
- Pull Request avant merge ;
- merge uniquement après validation qualité, sécurité et tests.

---

## 22. Définition de terminé

Une fonctionnalité est considérée terminée lorsque :
- le code est implémenté ;
- les tests associés existent et passent ;
- la couverture reste conforme ;
- les outils qualité passent ;
- la documentation est mise à jour ;
- le journal de développement est mis à jour ;
- les exceptions projet appropriées sont utilisées ;
- l’API publique concernée est stable et cohérente.

---

## 23. Recommandations de mise en œuvre pour l’IA de développement

L’IA de développement devra :
- développer en respectant strictement les contraintes du projet ;
- travailler par incréments cohérents ;
- éviter tout couplage dur avec le moteur de règles ;
- favoriser les objets métier explicites ;
- écrire les tests en même temps que les classes ;
- documenter les hypothèses de scoring ;
- privilégier l’explicabilité à la sophistication prématurée ;
- conserver Commander et Brawl comme points d’extension si non livrés immédiatement.

---

## 24. Résumé exécutable du MVP

Le MVP doit livrer, au minimum :
- un modèle de deck robuste ;
- un système de validation Construit / Limité ;
- un score heuristique détaillé ;
- une génération simple de decks candidats ;
- un système de mutation élémentaire ;
- une optimisation itérative simple ;
- une comparaison de decks ;
- une interface de simulation abstraite ;
- une suite de tests complète et conforme aux contraintes.

---

## 25. Orientation finale

`baobab-mtg-deckbuilder` doit devenir la brique métier qui répond à la question :
**« Quel est le meilleur deck possible à partir des cartes disponibles, sous des contraintes données, et pourquoi ? »**

Le projet doit être conçu pour fournir une réponse :
- valide,
- mesurable,
- explicable,
- reproductible,
- extensible.
