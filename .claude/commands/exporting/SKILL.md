# /exporting:SKILL — Export du Rapport Patrimonial

Génère un rapport patrimonial exportable via `python3 cgp/export.py`.

## Utilisation

```
/exporting:SKILL                          → HTML global (défaut)
/exporting:SKILL --format pdf             → PDF global
/exporting:SKILL --format png             → PNG (graphique d'allocation)
/exporting:SKILL --format html --scope financial  → HTML actifs financiers
/exporting:SKILL --format pdf --scope dca         → PDF section DCA
```

## Arguments

`$ARGUMENTS` peut contenir :
- `--format html` (défaut) | `--format pdf` | `--format png`
- `--scope global` (défaut) | `--scope financial` | `--scope dca`

## Instructions

1. Vérifier que `data/patrimoine.json` existe (outil Read)
2. Construire la commande : `python3 cgp/export.py $ARGUMENTS`
3. Exécuter avec l'outil Bash
4. Afficher le chemin du fichier généré

## Dépendances optionnelles

**PDF :**
```bash
pip install weasyprint
# Ubuntu/Debian : sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

**PNG :**
```bash
pip install cairosvg
```

## Après la génération

```
✅ Rapport exporté : exports/audit_global_20260627_143022.html

→ Ouvrir dans le navigateur pour consulter.
→ Pour PDF : /exporting:SKILL --format pdf
```
