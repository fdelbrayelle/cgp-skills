# /snapshotting:SKILL — Snapshot Mensuel du Patrimoine

Crée un instantané du patrimoine du mois en cours et le sauvegarde dans `data/history/YYYY-MM.json`.

À lancer une fois par mois, idéalement après avoir mis à jour les valeurs avec `/updating:SKILL`.

---

## Instructions

### Étape 1 — Lire et calculer

1. Lis `data/patrimoine.json` (outil Read)
2. Applique les formules de CLAUDE.md pour calculer :
   - `patrimoine_brut`
   - `patrimoine_net`
   - `passif_total`
   - Valeur de chaque classe d'actif : `immobilier`, `actions_pea`, `per`, `assurance_vie`, `scpi`, `or_physique`, `private_equity`, `crypto`, `livrets_liquidites`
   - Allocation actuelle en % de chaque classe
   - Plus-values latentes totales (PEA + crypto si disponibles)

### Étape 2 — Construire le snapshot

Construis le JSON suivant et sauvegarde-le dans `data/history/YYYY-MM.json` (ex : `data/history/2026-06.json`) :

```json
{
  "date": "YYYY-MM-DD",
  "mois": "YYYY-MM",
  "patrimoine_brut": XXXXX,
  "patrimoine_net": XXXXX,
  "passif_total": XXXXX,
  "dca_mensuel": XXXXX,
  "assets": {
    "immobilier": XXXXX,
    "actions_pea": XXXXX,
    "per": XXXXX,
    "assurance_vie": XXXXX,
    "scpi": XXXXX,
    "or_physique": XXXXX,
    "private_equity": XXXXX,
    "crypto": XXXXX,
    "livrets_liquidites": XXXXX
  },
  "allocation_pct": {
    "immobilier": XX.X,
    "actions_pea": XX.X,
    ...
  },
  "pv_latentes": {
    "pea": XXXXX,
    "crypto": XXXXX,
    "or_physique": XXXXX,
    "bspce": XXXXX
  },
  "bspce_pv_latente_totale": XXXXX
}
```

### Étape 3 — Vérifier les snapshots existants

Après la sauvegarde, lister les snapshots existants (Bash : `ls data/history/*.json 2>/dev/null | sort`) et afficher :

```
✅ Snapshot sauvegardé : data/history/2026-06.json

📅 HISTORIQUE DISPONIBLE
  2026-01.json  2026-02.json  2026-03.json  ...  2026-06.json
  → X mois de données  |  Évolution sur X mois : +XX XXX € (brut)

Lancez /auditing:SKILL pour voir l'analyse complète avec l'évolution historique.
```

---

## Automatisation

Le hook `.claude/settings.json` déclenche automatiquement `python3 cgp/snapshot.py --auto` après chaque appel à l'outil Write. Ce mode automatique :
- Vérifie que `data/patrimoine.json` existe
- Ne crée un snapshot que si le patrimoine brut a changé de plus de **100 €** par rapport au dernier snapshot du mois
- S'exécute silencieusement (erreurs redirigées vers `/dev/null`)

Ce skill `/snapshotting:SKILL` est donc utile pour forcer un snapshot manuel (ex. après une `/updating:SKILL` sans Write, ou pour un mois passé).

Pour forcer un snapshot sur un mois précis :
```bash
python3 cgp/snapshot.py --month 2026-05
```

Pour voir l'historique complet :
```bash
python3 cgp/snapshot.py --list
```

## Fréquence recommandée

- **Automatique** : à chaque modification de `patrimoine.json` via Claude Code
- **Manuel** : si vous modifiez `patrimoine.json` en dehors de Claude Code
- **À chaque événement majeur** : achat immobilier, souscription SCPI, gros DCA crypto

## Rotation des snapshots

Les snapshots sont conservés indéfiniment dans `data/history/`. Ils sont dans `.gitignore` et ne quittent pas la machine locale. En cas de suppression accidentelle, ils ne peuvent pas être récupérés depuis git.
