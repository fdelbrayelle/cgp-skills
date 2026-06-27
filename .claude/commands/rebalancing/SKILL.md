# /rebalancing:SKILL — Rééquilibrage DCA du Mois

Lis `data/patrimoine.json` (outil Read), calcule les drifts et détermine comment allouer le DCA mensuel. Si le fichier n'existe pas, demande d'exécuter `/initializing:SKILL`.

---

## Calculs à effectuer

1. **Patrimoine brut** et **allocation actuelle** (% par classe) — formules CLAUDE.md
2. **Drift** = `allocation_actuelle% − allocation_cible%`
3. **Classes DCA-compatibles uniquement** (rappel CLAUDE.md) :
   - ✅ Éligibles DCA : `actions_pea`, `per`, `assurance_vie`, `scpi` (PP en direct), `crypto`, `livrets_liquidites`
   - ❌ Non-DCA : `immobilier` (pas achetable mensuellement), `scpi nue_propriete` (achat ponctuel), `or_physique` (achat ponctuel), `private_equity` (souscription annuelle), `bspce` (illiquides, pas de flux mensuel possible)
4. **Allocation DCA** = proportionnelle aux drifts négatifs des classes éligibles uniquement

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

Classe                   │ Montant  │ % du DCA │ Barre
─────────────────────────────────────────────────────────────────────
Actions / PEA            │  X XXX € │   XX%    │ ██████████████░░░░░░░░
Épargne Retraite (PER)   │    XXX € │   XX%    │ █████░░░░░░░░░░░░░░░░░
SCPI (PP en direct)      │    XXX € │   XX%    │ ███░░░░░░░░░░░░░░░░░░░
─────────────────────────────────────────────────────────────────────
TOTAL                    │  X XXX € │  100%
```

### Conseils pratiques par enveloppe

**Actions / PEA — [broker]**
> Versez X XXX € sur votre PEA [broker].
> Marge disponible : XX XXX € / 150 000 €.
> Suggestion ETF : MSCI World (CW8, IWDA), ou Nasdaq (PANX) selon profil.
> Si PEA saturé → déborder sur CTO ou PEA-PME (plafond cumulé 225 000 €).

**PER — [assureur]**
> Versez XXX € sur votre PER [assureur].
> Économie d'impôt générée : XXX € (TMI [X]% × montant).
> Plafond déductible restant cette année : X XXX €.

**SCPI PP en direct**
> Les SCPI ont un ticket d'entrée élevé (1 part de 200 à 1 200 €).
> Si montant insuffisant → accumuler sur le mois et acheter une part le mois prochain.
> Réinvestissement des loyers activé : vérifier si les loyers perçus ce mois couvrent une part.

**Assurance Vie**
> Versez XXX € sur [nom contrat]. Préférer UC si horizon > 5 ans.

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
