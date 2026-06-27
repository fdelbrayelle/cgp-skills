# 💼 CGP Skills — Votre CGP Virtuel sous Claude Code

Gérez et pilotez votre patrimoine personnel directement depuis Claude Code, comme avec un **Conseiller en Gestion de Patrimoine (CGP)** à portée de clavier. L'outil est conçu pour les investisseurs français et couvre toutes les spécificités locales : PEA, PER, Assurance Vie, SCPI (pleine et nue-propriété), or physique, private equity, crypto.

---

## 🎯 Philosophie

Ce projet est **Claude-native** : les skills sont des prompts en français dans `.claude/commands/`. Claude lit votre patrimoine JSON, fait tous les calculs et produit une analyse experte. Zéro dépendance Python pour la logique métier.

Seul `cgp/export.py` utilise Python, pour générer des rapports HTML/PDF/PNG.

---

## 🚀 Démarrage rapide

### 1. Cloner le projet

```bash
git clone <votre-repo> cgp-skills
cd cgp-skills
```

### 2. Créer votre fichier de données

```bash
cp data/patrimoine.json.example data/patrimoine.json
# ⚠️ Ce fichier est dans .gitignore — vos données ne seront JAMAIS commitées
```

### 3. Lancer l'onboarding

Dans Claude Code (terminal ou IDE), tapez :

```
/initializing:SKILL
```

Claude vous guidera pas à pas (12 étapes) pour saisir :
- Profil investisseur : âge, risque, horizon, TMI, dépenses mensuelles, objectif FIRE
- Allocation cible par classe d'actifs
- Liquidités (Livret A, LDDS, LEP, compte courant)
- PEA (broker, date d'ouverture, composition)
- PER, Assurance Vie(s)
- SCPI pleine propriété et nue-propriété avec réinvestissement des loyers
- Or physique (pièces et lingots, prix d'achat moyen)
- Private Equity (FCPI, FIP, club deals)
- Crypto (BTC, ETH, altcoins, DeFi/staking, prix de revient)
- Immobilier (résidence principale avec indivision, locatif)

### 4. Lancer votre premier audit

```
/auditing:SKILL
```

---

## 📋 Skills disponibles

| Commande                | Description |
|-------------------------|-------------|
| `/initializing:SKILL`   | Onboarding complet — 12 étapes, toutes les classes d'actifs françaises |
| `/auditing:SKILL`       | Audit expert : allocation, règle 100−âge, règle des 4%, cash par profil, fiscalité |
| `/updating:SKILL`       | Mise à jour d'une valeur précise par menu numéroté (31 champs) |
| `/rebalancing:SKILL`    | Allocation optimale du DCA mensuel en euros par classe DCA-compatible |
| `/snapshotting:SKILL`   | Snapshot mensuel manuel → `data/history/YYYY-MM.json` |
| `/taxing:SKILL`         | Guide fiscal personnalisé par formulaire (2042, 2044, 2086, 3916-bis, 2092) |
| `/exporting:SKILL`      | Export rapport HTML / PDF / PNG |

---

## 🧠 Ce que fait `/auditing:SKILL`

L'audit est le cœur du projet. Il produit une analyse complète en 8 sections :

**1. Vue d'ensemble** — Patrimoine brut, net, passif, ratio

**2. Répartition** — Tableau allocation actuelle vs cible + barres Unicode visuelles pour 9 classes d'actifs

**3. Détail des actifs** — Analyse enveloppe par enveloppe :
- PEA : ancienneté, plus-value latente, marge de versement
- PER : économie d'impôt annuelle calculée à la TMI
- AV : ancienneté, statut abattement 8 ans
- SCPI PP : loyers nets après fiscalité, état du réinvestissement des loyers
- SCPI NP : illiquidité, date fin usufruit, plus-value de reconstitution estimée
- Or physique : option fiscale optimale calculée selon ancienneté (forfaitaire vs réelle)
- Private Equity : état de blocage, exonération PV si > 5 ans
- Crypto : détail BTC/ETH/altcoins, DeFi, plus-values latentes

**4. Analyse stratégique CGP** :
- 🎯 **Règle des 100 − âge** : `100 − âge` = % cible en actions (ex : 34 ans → 66% en actions)
- 📐 **Cohérence profil** : vos cibles vs les fourchettes de référence par profil
- 🏠 **Concentration immobilière** : alerte si RP > 50% du patrimoine brut
- 🛡️ **Réserve de précaution** : 2–6 mois de dépenses selon profil (calculé sur vos dépenses réelles)
- 💰 **Optimisation fiscale** : PER, PEA, AV, SCPI, or, PE, crypto

**5. Règle des 4%** — Indépendance financière :
- Revenu mensuel soutenable au taux 3,5% et 4%
- Capital manquant pour atteindre votre objectif FIRE
- Projection patrimoniale à [âge + horizon] ans avec DCA mensuel

**6. Analyse de liquidité** — Part illiquide (immobilier + SCPI NP + PE + or) vs limites par profil

**7. Score patrimonial /10** — Diversification, cohérence profil, enveloppes fiscales, réserve

**8. 3 actions prioritaires** — Concrètes et priorisées

---

## 💸 Ce que fait `/taxing:SKILL`

Le skill fiscal génère un guide personnalisé et structuré pour votre déclaration annuelle, formulaire par formulaire :

| Formulaire | Ce qui est couvert |
|------------|-------------------|
| **2042** | PER (cases 6DD/6RS/6QS), rachats AV après 8 ans, retraits PEA, dividendes CTO |
| **2044** | Revenus fonciers SCPI PP en direct — micro-foncier vs régime réel, conseil TMI |
| **2086** | Cessions crypto vers fiat — calcul PV, outils recommandés (Waltio, Koinly) |
| **3916-bis** | Exchanges étrangers à déclarer (Coinbase, Kraken...) — obligation annuelle |
| **2092** | Or physique — calcul comparatif option forfaitaire 11,5% vs PV réelle 36,2% |
| **Staking/DeFi** | Récompenses imposables en BNC (Lido, etc.) |
| **FCPI/FIP** | Exonération IR si > 5 ans de détention, PS 17,2% restants |
| **Checklist IFU** | Documents à récupérer auprès de chaque établissement |

Le skill commence par vous poser des questions sur vos transactions de l'année N-1 avant de générer le guide.

---

## 🔄 Workflow mensuel recommandé

```
1. /updating:SKILL    → Mettre à jour les soldes (PEA, crypto, or...)
2. /auditing:SKILL    → Analyser l'état du patrimoine
3. /rebalancing:SKILL → Savoir où mettre les X XXX €/mois de DCA
4. /exporting:SKILL   → Archiver le rapport du mois
```

**En période fiscale (avril-mai) :**
```
5. /taxing:SKILL      → Guide personnalisé par formulaire pour votre déclaration N-1
```

---

## 🇫🇷 Spécificités françaises intégrées

| Produit | Règles intégrées |
|---------|-----------------|
| **PEA** | Règle des 5 ans, plafond 150k€, 1/personne, calcul PV latente |
| **PER** | Déductibilité TMI, plafond 10% revenus, calcul économie d'impôt |
| **Assurance Vie** | Règle des 8 ans, abattement 4 600/9 200 €/an, avantage successoral |
| **SCPI PP** | Revenus nets après TMI + 17,2%, réinvestissement des loyers |
| **SCPI NP** | Illiquidité, zéro fiscalité pendant usufruit, revalorisation non imposable |
| **Or physique** | Option A (11,5% forfaitaire) vs Option B (36,2% sur PV réelle, abattement 5%/an) |
| **Private Equity** | Réduction IR 18-25% FCPI/FIP, exonération PV IR après 5 ans |
| **Crypto** | PFU 30%, échanges crypto/crypto non imposables, staking = BNC, 3916-bis |
| **Règle 100−âge** | Exposition actions recommandée = 100 − âge |
| **Règle des 4%** | SWR 3,5% (Europe) et 4% (Trinity Study), projection FIRE |

---

## 👥 Utiliser ce projet pour d'autres personnes

Ce projet peut être utilisé pour suivre le patrimoine de plusieurs personnes (famille, conjoint) en maintenant plusieurs fichiers JSON :

```bash
# Votre patrimoine
cp data/patrimoine.json.example data/patrimoine.json

# Patrimoine du conjoint (exemple)
cp data/patrimoine.json.example data/patrimoine_conjoint.json
```

> ⚠️ Ajoutez `data/patrimoine_*.json` à votre `.gitignore` pour protéger tous ces fichiers.

Pour qu'un autre utilisateur utilise ce projet sur sa propre machine :

1. **Cloner le repo** (ou copier les fichiers du projet)
2. **Ouvrir dans Claude Code** (`claude` dans le terminal depuis le dossier)
3. **Lancer** `/initializing:SKILL` pour créer son propre `data/patrimoine.json`
4. Les skills sont dans `.claude/commands/` → automatiquement disponibles dans Claude Code

### Structure des commandes Claude Code

Les skills sont stockés dans des dossiers nommés sous `.claude/commands/` :

```
.claude/commands/
  auditing/SKILL.md      → /auditing:SKILL
  initializing/SKILL.md  → /initializing:SKILL
  updating/SKILL.md      → /updating:SKILL
  rebalancing/SKILL.md   → /rebalancing:SKILL
  snapshotting/SKILL.md  → /snapshotting:SKILL
  taxing/SKILL.md        → /taxing:SKILL
  exporting/SKILL.md     → /exporting:SKILL
```

> **Note :** La syntaxe `dossier:fichier` est la convention Claude Code pour les sous-commandes.
> Le `CLAUDE.md` à la racine est chargé automatiquement comme contexte projet.

---

## 📁 Structure du projet

```
cgp-skills/
├── CLAUDE.md                         ← Instructions CGP + formules de calcul + référentiels
├── .claude/
│   └── commands/
│       ├── auditing/SKILL.md         ← /auditing:SKILL
│       ├── initializing/SKILL.md     ← /initializing:SKILL
│       ├── updating/SKILL.md         ← /updating:SKILL
│       ├── rebalancing/SKILL.md      ← /rebalancing:SKILL
│       ├── snapshotting/SKILL.md     ← /snapshotting:SKILL
│       ├── taxing/SKILL.md           ← /taxing:SKILL
│       └── exporting/SKILL.md        ← /exporting:SKILL
├── cgp/
│   ├── __init__.py
│   ├── export.py                     ← Export HTML/PDF/PNG
│   └── snapshot.py                   ← Historique automatique (hook PostToolUse)
├── data/
│   ├── patrimoine.json               ← VOS données (gitignored !)
│   ├── patrimoine.json.example       ← Template complet avec données fictives
│   └── history/                      ← Snapshots mensuels (gitignored)
├── exports/                          ← Rapports générés (gitignored)
├── requirements.txt
└── .gitignore
```

---

## 🔒 Sécurité & confidentialité

- `data/patrimoine.json` → dans `.gitignore` → **jamais commité**
- `exports/` → dans `.gitignore` → rapports non versionnés
- Aucune donnée transmise à des services tiers
- Tout reste sur votre machine locale

> ⚠️ Usage **strictement personnel**. Ne constitue pas un conseil financier professionnel réglementé.

---

## 📦 Export de rapports

HTML natif (aucune dépendance supplémentaire) :
```bash
python3 cgp/export.py --format html --scope global
```

PDF — installer weasyprint :
```bash
pip install weasyprint
# Ubuntu/Debian : sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
python3 cgp/export.py --format pdf
```

PNG — installer cairosvg :
```bash
pip install cairosvg
python3 cgp/export.py --format png --scope dca
```

Depuis Claude Code (plus simple) :
```
/exporting:SKILL --format pdf
/exporting:SKILL --format png --scope dca
```

---

*Fait avec ❤️ pour les investisseurs français qui prennent leur patrimoine en main.*
