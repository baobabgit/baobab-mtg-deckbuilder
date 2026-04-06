# Rapports de couverture

Ce répertoire accueille les **sorties générées** de `coverage` lorsque vous lancez les tests, par exemple :

```bash
python -m pytest
```

Fichiers et dossiers typiques (souvent ignorés par Git, voir `.gitignore`) :

- `html/` — rapport HTML interactif
- `coverage.xml` — export XML (CI, outils tiers)
- `.coverage` — fichier de données brut

La configuration (seuil minimal, chemins, exclusions) est définie dans `pyproject.toml`, sections `[tool.coverage.*]` et `[tool.pytest.ini_options]`.
