# /taxing:SKILL — Préparation de la Déclaration Fiscale

Lis `data/patrimoine.json` (outil Read) et génère un guide personnalisé et complet pour la déclaration d'impôts de l'année N-1.

Si le fichier n'existe pas, demande d'exécuter `/initializing:SKILL`.

---

## En-tête

```
═══════════════════════════════════════════════════════════════════
  💸 PRÉPARATION FISCALE [N] — [prenom_nom]
  Revenus de l'année [N-1] · TMI [tranche]% · [situation_familiale]
  ⚠️  Ce guide est informatif. Consultez un expert-comptable ou
      un CGP agréé pour votre déclaration officielle.
═══════════════════════════════════════════════════════════════════
```

---

## Étape 0 — Demander l'année et les transactions N-1

Avant de générer le guide, demande à l'utilisateur :

1. **Année concernée** (ex : déclaration 2025 pour les revenus 2024)
2. **Avez-vous effectué des retraits ou cessions en [N-1] ?**
   - PEA : retrait partiel ?
   - Assurance Vie : rachat partiel ou total ?
   - Crypto : ventes vers monnaie fiat (euros, dollars...) ?
   - Or physique : ventes de pièces ou lingots ?
   - SCPI NP : récupération de pleine propriété (fin d'usufruit) ?
   - Private Equity FCPI/FIP : cession ou liquidation de fonds ?
   - Immobilier locatif : vente ?
   - **BSPCE** : cession d'actions issues de l'exercice de BSPCE ?
3. **Montants versés sur le PER en [N-1]** (pour les déductions)

---

## Section 1 — FORMULAIRE 2042 (déclaration principale)

### PER — Versements déductibles (cases 6DD / 6RS / 6QS)

```
📋 FORMULAIRE 2042 — ÉPARGNE RETRAITE (PER)

  PER [assureur] — versements [N-1] : X XXX €

  ┌─────────────────────────────────────────────────────────────┐
  │  Case à cocher selon votre situation :                      │
  │  • Salarié        → Case 6DD (plafond = 10% salaire brut)  │
  │  • TNS/Indépendant→ Case 6RS ou 6QS (plafond majoré)       │
  │                                                              │
  │  Montant à saisir  : X XXX €                                │
  │  Économie d'impôt estimée (TMI [X]%) : X XXX €             │
  │  Plafond non utilisé reportable : X XXX € (case 6DD bis)   │
  └─────────────────────────────────────────────────────────────┘

  ✅ IFU fourni automatiquement par [assureur] en janvier-mars.
```

### Plus-values PEA (si retrait)

```
  Si retrait PEA en [N-1] :
  • PEA > 5 ans → gains EXONÉRÉS d'IR (mais PS 17,2% restent dus)
  • Case 2VM (prélèvements sociaux) ou cases Cerfa selon IFU Fortuneo
  ✅ IFU fourni par Fortuneo — saisir les montants indiqués.
```

### Plus-values Assurance Vie (si rachat)

```
  Si rachat AV en [N-1] :
  Gains imposables = (valeur rachetée / valeur totale AV) × versements nets
  
  Contrat [nom] ouvert le [date] :
  • [< 8 ans]  → PFU 30% sur les gains (12,8% IR + 17,2% PS)
  • [≥ 8 ans]  → Abattement [4 600 / 9 200]€, puis PFU 30% sur le surplus
               → Option : barème IR + PS 17,2% si plus avantageux

  ✅ IFU fourni par [assureur] — vérifier la rubrique "rachats imposables".
```

### Dividendes / Plus-values CTO (si applicable)

```
  Si CTO actif en [N-1] :
  • Dividendes → Case 2DC (PFU 30%) ou 2BH (barème sur option)
  • Plus-values → Case 3VG (PFU) ou barème sur option
  ✅ IFU fourni par le broker — copier les montants.
```

---

## Section 2 — FORMULAIRE 2044 (revenus fonciers) — SCPI pleine propriété en direct

```
📋 FORMULAIRE 2044 — REVENUS FONCIERS (SCPI EN DIRECT)

  ⚠️ S'applique uniquement aux SCPI en PLEINE PROPRIÉTÉ détenues EN DIRECT
     (pas à la nue-propriété et pas aux SCPI logées en AV)

  SCPI PP en direct — revenus bruts [N-1] estimés :
  • [Nom SCPI 1] : X XXX €/an bruts (rendement [X]% × valeur PP)
  • [Nom SCPI 2] :   XXX €/an bruts
  ────────────────────────────────────────────────
  Total revenus fonciers bruts : X XXX €

  CHOIX DU RÉGIME :
```

Calcule le régime optimal :

**Micro-foncier** (si revenus fonciers bruts ≤ 15 000 €/an) :
```
  → Abattement forfaitaire 30%
  → Revenus nets déclarés : X XXX × 70% = X XXX €
  → Case 4BE du formulaire 2042 (si micro-foncier)
  → Impôt estimé : X XXX € × (TMI [X]% + 17,2%) = X XXX €
```

**Régime réel** (si revenus > 15 000 € ou charges déductibles importantes) :
```
  → Formulaire 2044 complet (travaux, intérêts d'emprunt, frais de gestion...)
  → Recommandé si charges déductibles > 30% des revenus bruts
```

**Conseil personnalisé** :
```
  ┌─────────────────────────────────────────────────────────────┐
  │  À TMI [X]%, vos loyers SCPI vous coûtent :               │
  │  Imposition effective = [TMI + 17,2]% des revenus nets     │
  │  Soit ≈ X XXX € d'impôt sur X XXX € de loyers bruts       │
  │                                                              │
  │  💡 Si TMI ≥ 30% → envisager les prochaines SCPI en AV   │
  │     ou en nue-propriété pour supprimer cette imposition.    │
  └─────────────────────────────────────────────────────────────┘

  ✅ Les gestionnaires SCPI (Corum, Sofidy...) envoient un IFU
     avec le détail des revenus par SCPI et par pays.
     Certaines SCPI européennes ont des revenus imposables dans
     leur pays d'origine (convention fiscale bilatérale).
```

---

## Section 3 — FORMULAIRE 2086 (crypto-actifs)

```
📋 FORMULAIRE 2086 — CESSIONS DE CRYPTO-ACTIFS

  ⚠️ À remplir uniquement si vous avez vendu des cryptos contre
     des euros (ou autre monnaie fiat) en [N-1].
     Les échanges crypto-to-crypto ne sont PAS imposables.
```

Si l'utilisateur a eu des cessions :
```
  MÉTHODE DE CALCUL DE LA PLUS-VALUE :

  Pour chaque cession :
  PV = Prix de cession − (Prix de revient global × Prix cession / Valeur portefeuille au moment de la vente)

  Portfolio crypto au [date_mise_a_jour] :
  • BTC   : [quantité]  |  Coût d'acquisition total : X XXX €  |  Valeur actuelle : X XXX €
  • ETH   : [quantité]  |  Coût d'acquisition total : X XXX €  |  Valeur actuelle : X XXX €
  • SOL   : [quantité]  |  Coût d'acquisition total : X XXX €
  • Autres:              |  Valeur : X XXX €
  
  Prix de revient global du portefeuille : X XXX €
  
  Plus-values latentes totales : +X XXX €
  Taux d'imposition si cession : PFU 30% (12,8% IR + 17,2% PS)
  
  ⚠️ IMPORTANT : Pour chaque cession [N-1], il faut connaître :
    1. La valeur TOTALE du portefeuille au moment de la cession
    2. Le prix de cession de chaque actif vendu
    3. Le coût d'acquisition total cumulé depuis le début

  💡 Outil recommandé : Waltio, Koinly, ou CoinTracking pour
     générer automatiquement le formulaire 2086 à partir des
     historiques d'exchanges exportés en CSV.
```

Si aucune cession :
```
  ✅ Aucune cession vers fiat en [N-1] → formulaire 2086 non requis.
     Vos plus-values latentes (X XXX €) ne sont pas imposables
     tant que vous ne vendez pas.
```

**Récompenses DeFi/Staking** (si applicable) :
```
  Protocole [Lido (stETH)] — récompenses reçues en [N-1] :
  ⚠️ Les récompenses de staking sont imposables à leur valeur à la
     réception, comme des revenus (régime BNC ou revenus divers).
  → À déclarer en case [2TS ou BNC selon régime] du formulaire 2042.
  → Valeur approximative [N-1] à calculer depuis l'historique du protocole.
```

---

## Section 4 — FORMULAIRE 3916-bis (comptes étrangers)

```
📋 FORMULAIRE 3916-bis — COMPTES DÉTENUS À L'ÉTRANGER

  OBLIGATION : À déclarer si vous détenez des comptes sur des
  plateformes étrangères, même sans transaction en [N-1].

  Exchanges à déclarer :
```

Pour chaque exchange étranger détecté dans les données :
```
  • Coinbase (siège : États-Unis)
    Nom de l'organisme : Coinbase Inc.
    Pays : USA
    Type de compte : Compte crypto (achat/vente/conservation)
    → Une ligne par exchange, même si le solde est 0.

  • Kraken (siège : États-Unis)
    ...

  ✅ Ledger (hardware wallet français) → PAS à déclarer
     (portefeuille physique, pas un compte chez un organisme étranger)

  ℹ️ Formulaire intégré dans la déclaration en ligne impots.gouv.fr
     (section "Comptes à l'étranger" — accessible depuis 2042).
     Amende si non déclaré : 750 € par compte non déclaré.
```

---

## Section 5 — OR PHYSIQUE (si vente en [N-1])

```
📋 OR PHYSIQUE — TAXE SUR MÉTAUX PRÉCIEUX

  [Si vente de pièces/lingots en [N-1] :]

  Votre portefeuille or :
  • [X] Napoléons  → Valeur de cession : X XXX €
  • [X] Souverains → Valeur de cession : X XXX €
  • [X]g lingot    → Valeur de cession : X XXX €

  CALCUL COMPARATIF :

  Option A — Taxe forfaitaire (défaut) :
    11,5% × prix de cession total = X XXX €
    Payée par le revendeur (acheteur professionnel) en général.
    Pas de formulaire IR à remplir.

  Option B — Sur la plus-value réelle :
    PV = prix cession − prix d'acquisition
    Abattement : [N] années de détention × 5% dès la 3e année
    [N] ans → abattement [N×5 − 10]% → PV imposable = X XXX €
    Impôt = PV imposable × 36,2%
    Formulaire : 2092 (Taxe sur la plus-value des métaux précieux)

  ✅ Option recommandée pour votre situation :
    Option [A ou B] → économie estimée : X XXX €
    [Détail du calcul avec les dates et prix d'acquisition réels]
```

---

## Section 6 — BSPCE (si cession d'actions issues de BSPCE en [N-1])

```
📋 BSPCE — BONS DE SOUSCRIPTION DE PARTS DE CRÉATEUR D'ENTREPRISE

  ⚠️ À remplir uniquement si vous avez cédé des actions issues de l'exercice
     de vos BSPCE en [N-1]. L'exercice seul (sans cession) n'est pas imposable.
```

Si l'utilisateur a eu des cessions d'actions BSPCE :

```
  CALCUL DU GAIN NET :

  Gain BSPCE = Prix de cession − Prix d'exercice

  TAUX D'IMPOSITION — selon l'âge de l'entreprise à la date d'ATTRIBUTION :

  ┌─────────────────────────────────────────────────────────────────┐
  │  [Entreprise < 3 ans à l'attribution]                           │
  │  → PFU 30% : 12,8% IR + 17,2% PS                               │
  │  Gain imposable : X XXX €  |  Impôt estimé : X XXX €           │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │  [Entreprise ≥ 3 ans à l'attribution] ← cas le plus courant    │
  │  → 17,2% PS UNIQUEMENT — exonéré d'IR ✅                        │
  │  Gain imposable : X XXX €  |  Impôt estimé : X XXX € (PS seul) │
  └─────────────────────────────────────────────────────────────────┘

  SI GAIN DE CESSION SUPPLÉMENTAIRE (prix vente > valeur au jour d'exercice) :
  → Ce surplus est traité comme une plus-value mobilière → PFU 30%
  → Cases 3VG du formulaire 2042

  DÉCLARATION :
  → Le gain BSPCE figure sur l'IFU ou l'attestation fiscale de l'entreprise
  → En l'absence d'IFU, calcul manuel : (prix cession − prix exercice) × nombre d'actions
  → Case 1TZ (gain exonéré d'IR, PS dues) ou cases ordinaires selon situation
  → Vérifier avec un expert-comptable pour les cas complexes (M&A, liquidité partielle)

  ✅ Si aucune cession : plus-values BSPCE 100% latentes → aucune imposition,
     aucune déclaration à effectuer.
```

---

## Section 7 — PRIVATE EQUITY (si cession/liquidation en [N-1])

```
📋 PRIVATE EQUITY — FCPI/FIP

  [Nom fonds] — souscrit en [vintage], [ancienneté] ans de détention

  Si cession ou liquidation en [N-1] :
  • [< 5 ans de détention] → PV imposée au PFU 30%
  • [≥ 5 ans de détention] → PV EXONÉRÉE d'IR ✅
                              Prélèvements sociaux 17,2% restent dus

  Montant à déclarer : (produit de cession − montant souscrit) × 17,2%
  → Cases du formulaire 2042 selon l'IFU du gestionnaire de fonds.

  ℹ️ La réduction IR à l'entrée (X XXX €) a déjà été déduite
     sur la déclaration de l'année de souscription ([vintage]).
```

---

## Section 8 — CHECKLIST FINALE

```
✅ RÉCAPITULATIF — CE QUE VOUS AVEZ À FAIRE

DOCUMENTS À RÉCUPÉRER (janvier-mars [N]) :
  □ IFU Fortuneo (PEA)               — [adresse réception ou espace client]
  □ IFU Linxea Avenir 2 (AV)         — [si rachat en [N-1]]
  □ IFU PER Linxea Spirit 2          — versements déductibles
  □ Relevés SCPI (Corum, Remake Live) — revenus par SCPI, par pays
  □ Historiques exchanges (Coinbase, Kraken) → export CSV pour Waltio/Koinly
  □ Relevé gestionnaire PE (Eurazeo) — si distribution/liquidation

FORMULAIRES À REMPLIR :
  □ 2042    — PER (case 6DD : X XXX €)
  □ 2042    — BSPCE [si cession d'actions en [N-1]] (case 1TZ ou 3VG selon situation)
  □ 2044    — SCPI en direct [si revenus > 0] (revenus bruts : X XXX €)
  □ 2086    — Crypto [si cessions vers fiat en [N-1]]
  □ 3916-bis— Coinbase, Kraken [obligation annuelle]
  □ 2092    — Or physique [si vente en [N-1]]

DATES CLÉS :
  □ Mai [N]     — Date limite déclaration en ligne (zones A, B, C)
  □ 31 déc [N]  — Dernier jour pour verser sur PER et réduire l'IR de [N]

OPTIMISATIONS AVANT FIN D'ANNÉE [N] :
  □ Maximiser PER : plafond restant X XXX € → économie IR potentielle X XXX €
  □ Souscription FCPI/FIP avant le 31 décembre → réduction IR 18%

─────────────────────────────────────────────────────────────────
⚠️  Ce guide est généré à partir de données statiques dans
    patrimoine.json. Il ne remplace pas l'accompagnement d'un
    expert-comptable ou d'un CGP agréé CIF. Les montants exacts
    dépendent de vos transactions réelles de l'année [N-1].
```
