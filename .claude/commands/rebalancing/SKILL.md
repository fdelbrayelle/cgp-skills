# /rebalancing:SKILL — Rééquilibrage DCA du Mois

Lis `data/patrimoine.json` (outil Read), calcule les drifts et détermine comment allouer le DCA mensuel. Si le fichier n'existe pas, demande d'exécuter `/initializing:SKILL`.

---

## Calculs à effectuer

1. **Patrimoine brut** et **allocation actuelle** (% par classe) — formules CLAUDE.md
2. **Drift** = `allocation_actuelle% − allocation_cible%`
3. **Classes DCA-compatibles uniquement** (rappel CLAUDE.md) :
   - ✅ Éligibles DCA : `actions_pea`, `per`, `assurance_vie`, `scpi` (PP en direct), `crypto`, `livrets_liquidites`
   - ❌ Non-DCA : `immobilier` (pas achetable mensuellement), `scpi nue_propriete` (achat ponctuel), `or_physique` (achat ponctuel), `private_equity` (souscription annuelle), `bspce` (illiquides, pas de flux mensuel possible)
4. **DCA programmés** : lire `versement_mensuel_programme` sur chaque enveloppe (pea, per, chaque contrat AV, scpi.pleine_propriete.en_direct, crypto). Sommer les non-null → `total_programme`.
5. **Allocation DCA** :
   - Si `total_programme > 0` : les montants programmés sont affichés en priorité (colonne "Programmé") ; le solde `dca_mensuel_cible − total_programme` est distribué proportionnellement aux drifts négatifs des classes éligibles sans montant programmé (colonne "Drift")
   - Si `total_programme = 0` : allocation 100% proportionnelle aux drifts négatifs (comportement historique)
   - Si `total_programme > dca_mensuel_cible` → afficher alerte rouge ⛔

---

## Format d'affichage

### En-tête

```
════════════════════════════════════════════════════════════
  🔄 RÉÉQUILIBRAGE DCA — [prenom_nom]
  [mois courant] · DCA mensuel : X XXX €/mois
  Règle 100−âge : à [age] ans → cible actions ~[100-age]%
════════════════════════════════════════════════════════════
```

### Contexte macro-économique

Utilise **WebSearch** pour identifier le régime macro actuel (< 30 jours) : inflation IPC zone euro + croissance PIB France/zone euro. Positionne en une ligne dans l'en-tête du rapport :

```
🌐 RÉGIME MACRO : [🔥 Inflationary Boom | 🚀 Disinflationary Boom | 🌡️ Stagflation | 🧊 Deflationary Bust]
   Inflation : X,X% (zone euro) │ PIB : X,X% │ Source : [BCE/Eurostat, mois année]
   → [1 phrase d'impact sur l'allocation DCA de ce mois — ex. "Régime favorable aux actions, prioriser PEA"]
```

Ce contexte oriente les commentaires par enveloppe ci-dessous :
- **Disinflationary Boom** → renforcer actions PEA / UC / PE ; limiter excès de liquidités
- **Inflationary Boom** → favoriser SCPI PP, or ponctuel, immobilier ; fonds euros sous-performe
- **Stagflation** → prudence actions, or et liquidités courtes en refuge ; DCA actions maintenu sur long terme
- **Deflationary Bust** → fonds euros et livrets en priorité ; limiter PE et crypto

---

### Tableau des drifts

```
📊 ÉTAT DU PORTEFEUILLE

Classe d'actif           │ Actuel │ Cible │   Drift    │ DCA-compat │ Action
───────────────────────────────────────────────────────────────────────────────
Immobilier               │  XX.X% │  XX%  │  +XX.X% ↑  │     ❌     │ Conserver
Actions / PEA            │  XX.X% │  XX%  │   −X.X% ↓  │     ✅     │ 🟠 Abonder
Épargne Retraite (PER)   │   X.X% │   X%  │   −X.X% ↓  │     ✅     │ 🟠 Abonder
Assurance Vie            │  XX.X% │  XX%  │   +X.X% ↑  │     ✅     │ Conserver
SCPI (PP en direct)      │   X.X% │   X%  │   −X.X% ↓  │     ✅     │ 🟠 Abonder
SCPI (NP)                │   X.X% │        │    N/A      │     ❌     │ Achat ponctuel
Or physique              │   X.X% │   X%  │   +X.X% ↑  │     ❌     │ Achat ponctuel
Private Equity           │   X.X% │   X%  │   −X.X% ↓  │     ❌     │ Souscription fin d'année
Crypto                   │   X.X% │   X%  │   +X.X% ↑  │     ✅     │ Conserver
Livrets & Liquidités     │   X.X% │   X%  │   +X.X% ↑  │     ✅     │ Conserver
```

### Allocation du DCA en euros

```
💶 ALLOCATION DU DCA — X XXX €/mois
   Programmé : X XXX € · Solde drift : XXX €

Classe                   │ Programmé │  Drift  │  TOTAL   │ Barre
──────────────────────────────────────────────────────────────────────
Actions / PEA            │   800 €   │   —     │   800 €  │ ██████████████░░░░
Épargne Retraite (PER)   │   200 €   │   —     │   200 €  │ ████░░░░░░░░░░░░░░
Assurance Vie            │   300 €   │  200 €  │   500 €  │ ████████░░░░░░░░░░
SCPI (PP en direct)      │    —      │    —    │    —     │ (accumulation)
──────────────────────────────────────────────────────────────────────
TOTAL                    │ X XXX €   │  XXX €  │ X XXX €
```

> Si `versement_mensuel_programme` est null pour une classe DCA-compatible sous-pondérée, le solde drift lui est alloué normalement.
> Si toutes les enveloppes ont un montant programmé et que le solde drift est nul, afficher le tableau sans la colonne Drift.

### Conseils pratiques par enveloppe

**Actions / PEA — [broker]**
> Versez X XXX € sur votre PEA [broker] (dont XXX € programmés + XXX € drift).
> Marge disponible : XX XXX € / 150 000 €.
> Suggestion ETF : MSCI World (CW8, IWDA), ou Nasdaq (PANX) selon profil.
> Si PEA saturé → déborder sur CTO ou PEA-PME (plafond cumulé 225 000 €).

**PER — [assureur]**
> Versez XXX € sur votre PER [assureur] (dont XXX € programmés + XXX € drift).
> Économie d'impôt générée : XXX € (TMI [X]% × montant).
> Plafond déductible restant cette année : X XXX €.

**SCPI PP en direct**
> Les SCPI ont un ticket d'entrée élevé (1 part de 200 à 1 200 €).
> Si montant insuffisant → accumuler sur le mois et acheter une part le mois prochain.
> Réinvestissement des loyers activé : vérifier si les loyers perçus ce mois couvrent une part.

**Assurance Vie — [nom contrat]**
> Versez XXX € sur [nom contrat] (dont XXX € programmés + XXX € drift). Préférer UC si horizon > 5 ans.

### Alertes spéciales

Vérifie et affiche si pertinent :

- **PEA proche de la saturation** (versements_cumules > 130 000 €) → signaler les 20 000 € restants
- **PER non ouvert** et TMI ≥ 30% → fort conseil d'ouverture immédiate
- **Règle 100−âge non respectée** → indiquer le delta en € à orienter vers actions ce mois
- **SCPI NP à surveiller** → si fin d'usufruit dans < 3 ans, anticiper la gestion de la pleine propriété
- **Or physique sous-pondéré** → noter que l'achat doit être planifié (pas DCA mensuel) ; budget achat suggéré
- **Private Equity** : si fin d'année fiscale dans < 3 mois → rappeler la possibilité de souscription FCPI/FIP (réduction IR [X]%)
- **Crypto sur-pondérée** et en forte plus-value → suggérer prise de profit partielle et réinvestissement

### Portefeuille équilibré

Si aucune classe DCA-compatible n'est sous-pondérée :

```
✅ PORTEFEUILLE ÉQUILIBRÉ

Investissez votre DCA X XXX €/mois proportionnellement à vos cibles :
  Actions / PEA    → X XXX €  (XX% × X XXX €)
  PER              →   XXX €  (X% × X XXX €)
  ...

→ Profitez-en pour vérifier si un achat ponctuel d'or ou de SCPI NP
  est pertinent pour les classes non-DCA en drift négatif.
```

---

## Pied de page

```
💡 Le rééquilibrage via DCA est la méthode la plus fiscalement efficace
   (pas de cession imposable). Préférez toujours orienter les nouveaux
   investissements vers les classes sous-pondérées plutôt que de vendre.

→ /exporting:SKILL pour générer un rapport de ce rééquilibrage
```
