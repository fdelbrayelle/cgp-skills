# /auditing:SKILL — Audit Patrimonial Complet

Lis `data/patrimoine.json` (outil Read), applique les formules de calcul définies dans CLAUDE.md, puis affiche l'audit complet ci-dessous. Si le fichier n'existe pas, demande d'exécuter `/initializing:SKILL`.

---

## Format d'affichage

### En-tête

```
════════════════════════════════════════════════════════════
  💼 AUDIT PATRIMONIAL — [prenom_nom]
  Profil [profil_risque] · [age] ans · Horizon [horizon] ans
  TMI [tranche]% · Mis à jour le [date_mise_a_jour]
════════════════════════════════════════════════════════════
```

---

### 1. Vue d'ensemble

```
📊 PATRIMOINE GLOBAL
┌─────────────────────────────────────────────────┐
│  Patrimoine Brut     :  XXX XXX €               │
│  Passif (crédits)    :   −XX XXX €              │
│  Patrimoine Net      :  XXX XXX €               │
│  Ratio Net/Brut      :  XX.X%                   │
└─────────────────────────────────────────────────┘
```

---

### 2. Répartition des actifs

Calcule chaque classe selon les formules de CLAUDE.md (ne pas doubler les SCPI en AV).

```
📈 RÉPARTITION DES ACTIFS (sur patrimoine brut)

Classe d'actif         │ Valeur      │ Actuel │ Cible │  Écart   │ Statut
───────────────────────────────────────────────────────────────────────────
Immobilier             │ XXX XXX €   │  XX.X% │  XX%  │ +XX.X%   │ ↑ Sur-pondéré
Actions / PEA          │  XX XXX €   │  XX.X% │  XX%  │ −XX.X%   │ ↓ Sous-pondéré
Épargne Retraite (PER) │  XX XXX €   │   X.X% │   X%  │  ±X.X%   │ ≈ Équilibré
Assurance Vie          │  XX XXX €   │  XX.X% │  XX%  │  −X.X%   │ ↓ Sous-pondéré
SCPI                   │  XX XXX €   │   X.X% │   X%  │  −X.X%   │ ↓ Sous-pondéré
Or physique            │  XX XXX €   │   X.X% │   X%  │  ±X.X%   │ ≈ Équilibré
Private Equity         │   X XXX €   │   X.X% │   X%  │  −X.X%   │ ↓ Sous-pondéré
Crypto                 │  XX XXX €   │   X.X% │   X%  │  +X.X%   │ ↑ Sur-pondéré
Livrets & Liquidités   │  XX XXX €   │   X.X% │   X%  │  +X.X%   │ ↑ Sur-pondéré
───────────────────────────────────────────────────────────────────────────
TOTAL                  │ XXX XXX €   │ ~100%
```

Barres visuelles Unicode (proportionnelles sur 32 chars) :

```
Immobilier      ██████████████████░░░░░░░░░░░░░░  XX%
Actions / PEA   ████████░░░░░░░░░░░░░░░░░░░░░░░░  XX%
...
```

Légende : `↑ Sur-pondéré` `↓ Sous-pondéré` `≈ Équilibré (±2%)`

---

### 3. Détail des enveloppes & actifs

#### 3a. Enveloppes fiscales

**PEA — [broker]**
```
  Ouverture : [date]  |  Ancienneté : X ans X mois
  Valeur actuelle   : XX XXX €
  Versements cumulés: XX XXX €   (marge restante : XX XXX € / 150 000 €)
  Plus-value latente: +X XXX € (+XX%)
  [⚠️ < 5 ans — un retrait ferme définitivement le compte]
  [✅ > 5 ans — retraits partiels sans fermeture, gains exonérés d'IR]
```

**PER — [assureur]**
```
  Valeur totale : XX XXX €  (fonds euros : X XXX € | UC : XX XXX €)
  Déduction max : X XXX €/an   Économie impôt à TMI [tranche]% : X XXX €/an
```

**Assurance Vie(s)**
```
  [nom] — [assureur]  |  Ouverture : [date]
  Fonds euros : X XXX € | UC : XX XXX € | Total : XX XXX €
  [⚠️ < 8 ans — abattement fiscal sur gains non encore disponible]
  [✅ > 8 ans — abattement [4600/9200]€/an disponible sur les gains]
```

#### 3b. SCPI — analyse détaillée

**SCPI Pleine Propriété en direct**
```
  Valeur totale PP : XX XXX €
  Loyers bruts estimés : XX €/mois  →  XXX €/an
  Loyers nets après fiscalité (TMI [tranche]% + 17,2% PS) : XX €/mois
  [Réinvestissement des loyers : OUI → les loyers rachètent des parts automatiquement]
  [Réinvestissement des loyers : NON → loyers versés sur le compte bancaire]

  Détail par SCPI :
  • [Nom SCPI] : [nb] parts × [valeur/part] = X XXX €  |  Rendement [X]%  |  Loyers [X]€/an
```

**SCPI Nue-Propriété**
```
  Valeur totale NP (prix acquisition) : XX XXX €
  ⚠️ Actif ILLIQUIDE — aucun loyer jusqu'à fin d'usufruit
  
  • [Nom SCPI NP] : [nb] parts × [prix NP] = X XXX €
    PP estimée : X XXX €  |  Décote NP : [X]%
    Fin d'usufruit : [date]  →  Plus-value de reconstitution estimée : +X XXX € (non imposable)
```

**SCPI via Assurance Vie**
```
  Incluses dans la valeur de l'AV [nom contrat] — aucune imposition directe sur les loyers.
```

#### 3c. Or physique

```
🥇 OR PHYSIQUE
  Valeur totale : XX XXX €

  Pièces :
  • [X] Napoléons 20F  × [valeur spot]€  =  X XXX €  (achat moyen : X€/pièce — PV latente : +X€)
  • [X] Souverains     × [valeur spot]€  =  X XXX €

  Lingots :
  • [X]g  valeur spot X XXX €  (achat : X XXX € — PV latente : +X XXX €)

  Stockage : [détail]
  
  Fiscalité à la vente :
  Option A (forfaitaire) : 11,5% × prix de cession
  Option B (réelle)      : 36,2% sur PV − abattement 5%/an dès la 3e année
  → Recommandation si détenu depuis [N] ans : [option avantageuse + calcul]
```

#### 3d. Private Equity

```
🚀 PRIVATE EQUITY
  Valeur totale estimée : X XXX €
  ⚠️ Actifs ILLIQUIDES jusqu'à fin de période de blocage

  FCPI/FIP :
  • [Nom] ([type], vintage [année])
    Souscription : X XXX €  |  VL actuelle : X XXX €
    Réduction IR obtenue : X XXX € ([X]% de [montant])
    Fin blocage estimée : [date]  |  Exonération PV IR après 5 ans : [oui/non selon ancienneté]
```

#### 3e. Crypto

```
₿ CRYPTO-ACTIFS
  Valeur totale : XX XXX €
  Plus-value latente totale : +X XXX € (base d'acquisition : X XXX €)

  Allocation interne :
  • BTC : X,XXX  →  XX XXX € (XX% du portfolio crypto)  |  PV latente : +X XXX €
  • ETH : X,X    →   X XXX € (XX% du portfolio crypto)  |  PV latente : +X XXX €
  • [Ticker] : ...
  • Autres    :   X XXX € (XX%)

  DeFi / Staking :
  • [Protocole] : X XXX € | Rendement ~X%/an (⚠️ récompenses imposables à la réception — BNC)

  Exchanges / Wallets : [liste]
  ⚠️ Exchanges étrangers → déclaration formulaire 3916-bis obligatoire
```

---

### 4. Analyse stratégique CGP

#### 4a. Règle des 100 − âge (exposition actions)

Calcule et affiche :

```
🎯 RÈGLE DES 100 − ÂGE

  À [age] ans → exposition actions recommandée : [100 - age]%
  (variantes : [110 - age]% profil offensif / [90 - age]% profil prudent)

  Votre exposition actions actuelle     : XX.X%  (PEA + PEA-PME + CTO)
  Exposition croissance (actions+crypto): XX.X%  (y compris PE, actifs risqués)
  Recommandation règle des 100 − âge   : [100 - age]%
```

Évalue l'écart :
- Si `exposition_actions < (100 - age) - 5` → signal rouge (sous-exposé selon âge)

  > **🔴 Sous-exposition actions significative**
  > À [age] ans, la règle des 100 − âge recommande ~[100-age]% en actions.
  > Votre exposition est de XX% — vous laissez de la performance sur la table.
  > Avec [horizon] ans devant vous, le temps est votre meilleur allié pour lisser la volatilité.

- Si dans la fourchette (±5%) → signal vert
- Si exposition > (100 - age) + 10% → suggérer de sécuriser progressivement

#### 4b. Cohérence profil / allocation cible

Compare l'allocation cible de l'utilisateur aux fourchettes de référence (CLAUDE.md). Pour chaque classe hors fourchette, signale-le avec explication. Exemple :

> **⚠️ Or physique** : votre cible est 8%, mais un profil Dynamique recommande 2–5%.
> L'or est une assurance, pas un moteur de croissance — une surpondération pénalise le rendement long terme.

#### 4c. Concentration immobilière

Si `immobilier_pct > 50%` :

> **🏠 Forte concentration immobilière ([X]%)**
> Votre résidence principale représente [X]% du patrimoine brut mais génère ZÉRO revenu
> et est totalement illiquide. Votre patrimoine financier "actif" n'est que de XX XXX €.
> Objectif : augmenter progressivement la part financière via le DCA mensuel.

#### 4d. Réserve de précaution

Calcule la réserve cible selon le profil et les dépenses mensuelles déclarées.

Si `depenses_mensuelles` est défini dans le profil :
```
  mois_cible :
    Prudent   → 5–6 mois  (target = depenses × 5.5)
    Équilibré → 4–5 mois  (target = depenses × 4.5)
    Dynamique → 3–4 mois  (target = depenses × 3.5)
    Offensif  → 2–3 mois  (target = depenses × 2.5)
```

Sinon, utiliser `dca_mensuel_cible × 4` comme proxy.

Affiche :
```
🛡️ RÉSERVE DE PRÉCAUTION

  Dépenses mensuelles : X XXX €/mois
  Réserve cible (profil [profil]) : X XXX € ([X–Y] mois)
  Liquidités actuelles            : XX XXX €
  Couverture actuelle             : X.X mois
```

- Si `liquidites < depenses × 3` → alerte ROUGE priorité absolue :
  > ⚠️ MATELAS DE SÉCURITÉ INSUFFISANT — XX XXX € couvrent seulement X.X mois.
  > Reconstituer ce matelas AVANT tout nouvel investissement.

- Si liquidites entre target et target × 1.5 → ✅ réserve correctement dimensionnée

- Si `liquidites > target × 1.5` → cash drag :
  > 💤 CASH DRAG : X XXX € de trop en liquidités.
  > Excédent investissable : X XXX € → orienter selon /rebalancing:SKILL.

#### 4e. Optimisation fiscale

**PER** :
- Si TMI ≥ 30% et versements annuels < plafond :
  > **💰 PER sous-utilisé** : à TMI [X]%, versez X XXX €/an de plus → X XXX € d'économie d'impôt immédiate.

**PEA non ouvert** → fort conseil d'ouverture immédiate.

**AV > 8 ans** → rappeler la disponibilité de l'abattement.

**SCPI en direct + TMI ≥ 30%** :
  > **⚠️ Fiscalité SCPI** : vos loyers sont imposés à [TMI+17,2]%. Envisagez de loger les prochaines SCPI en AV ou PER.

**SCPI NP + TMI élevée** → valoriser le choix (zéro fiscalité pendant l'usufruit).

**Or physique** → calculer l'option la plus avantageuse à la vente selon ancienneté de détention.

**Private Equity** :
- Si ancienneté > 5 ans → rappeler que les PV sont exonérées d'IR (PS 17,2% restants)
- Si fin d'année fiscale approche → suggérer souscription FCPI/FIP avant 31/12 pour réduction IR

**Crypto** :
- Si plus-values latentes importantes → suggérer de lisser les cessions (rester sous le seuil annuel si possible)
- Rappeler : échanges crypto-to-crypto non imposables, cessions vers fiat imposables

**Or + Crypto** → rappeler la déclaration annuelle 2086 (crypto) et formulaire 3916-bis (exchanges étrangers)

---

### 5. Règle des 4% — Indépendance Financière

Applique la Safe Withdrawal Rate (SWR) sur le patrimoine NET :

```
💰 RÈGLE DES 4% — INDÉPENDANCE FINANCIÈRE (FIRE)

  Patrimoine net actuel               :   XXX XXX €
  ─────────────────────────────────────────────────
  Revenu mensuel soutenable (SWR 4%)  :   X XXX €/mois  (prudent Europe : 3,5% → X XXX €/mois)
```

Si `objectif_revenu_mensuel_eur` est défini et > 0 :
```
  Objectif revenu mensuel passif      :   X XXX €/mois
  [Moins pension retraite estimée]    :  −X XXX €/mois   (si pension_retraite définie)
  Revenu à couvrir par le capital     :   X XXX €/mois

  Capital nécessaire (règle 4%)       : X XXX XXX €
  Capital encore à constituer         :   XXX XXX €

  Projection DCA — scénario [X]%/an de rendement estimé :
    Dans [Y] ans (à [age+Y] ans) → patrimoine projeté ~X XXX XXX €
    Revenu mensuel potentiel          :   X XXX €/mois
    [✅ Objectif FIRE atteignable dans votre horizon] OU [⚠️ Nécessite d'accélérer le DCA]
```

Pour estimer le rendement projeté, utilise selon le profil :
- Prudent : 3–4%/an net
- Équilibré : 4–6%/an net
- Dynamique : 6–8%/an net
- Offensif : 8–10%/an net (volatilité élevée)

Note : la règle des 4% suppose un portefeuille 60% actions / 40% obligations sur 30 ans (étude Trinity). Adapte à la composition réelle et à l'horizon.

---

### 6. Illiquidité du patrimoine

Calcule et affiche la part d'actifs illiquides :

```
🔒 ANALYSE DE LA LIQUIDITÉ

  Actifs liquides (< 1 semaine)     : XX XXX €  (XX%)  — Livrets, crypto, PEA > 5 ans
  Actifs semi-liquides (< 3 mois)   : XX XXX €  (XX%)  — AV, PER, actions cotées
  Actifs illiquides (> 1 an)        : XX XXX €  (XX%)  — Immobilier, SCPI NP, PE, or

  Limite recommandée illiquidité : [20% Prudent / 30% Équilibré / 35% Dynamique]%
  Votre illiquidité actuelle     : XX.X%  [OK / ⚠️ Dépasse la limite recommandée]
```

---

### 7. Score patrimonial

Score sur 10, calculé selon :
- **Diversification** (≥ 5 classes représentées + or ou PE) : /3
- **Cohérence profil/allocation** (règle 100−âge + fourchettes profil) : /3
- **Enveloppes fiscales** (PEA ouvert, PER utilisé si TMI ≥ 30%, AV active) : /2
- **Réserve de précaution** (dans la bonne fourchette pour le profil) : /2

```
⭐ SCORE PATRIMONIAL : X.X / 10
[██████████] Diversification      : X/3
[████████░░] Cohérence profil     : X/3
[████░░░░░░] Enveloppes fiscales  : X/2
[████████░░] Réserve précaution   : X/2

→ Points prioritaires : [2-3 actions les plus impactantes]
```

---

### 8. Évolution historique

Avant d'afficher cette section, exécute (outil Bash) :
```bash
ls data/history/*.json 2>/dev/null | sort
```

**Si aucun fichier** :
```
📅 HISTORIQUE
  Aucun snapshot disponible.
  → Lancez /snapshotting:SKILL après cet audit pour démarrer le suivi mensuel.
```

**Si des snapshots existent** :
Lis les fichiers (jusqu'aux 12 derniers) avec l'outil Read et affiche :

```
📅 ÉVOLUTION DU PATRIMOINE (12 derniers mois)

Mois      │ Brut        │ Net         │ Actions    │ Crypto     │ Δ Brut/mois
──────────────────────────────────────────────────────────────────────────────
2025-07   │  280 000 €  │  180 000 €  │  38 000 €  │  15 000 €  │    —
2025-08   │  283 000 €  │  183 500 €  │  39 500 €  │  14 200 €  │ +3 000 €
2025-09   │  286 000 €  │  186 000 €  │  41 000 €  │  14 800 €  │ +3 000 €
...
2026-06   │  312 000 €  │  206 000 €  │  51 000 €  │  21 500 €  │ +11 000 € 🚀
──────────────────────────────────────────────────────────────────────────────
Évolution  │ +32 000 €   │ +26 000 €   │ +13 000 €  │ +6 500 €
sur 12 mois│ (+11,4%)    │ (+14,4%)    │ (+34,2%)   │ (+43,3%)
```

Calcule et affiche :
- **Rythme d'accumulation moyen** : Δ brut moyen par mois
- **Projection à [horizon] ans** au rythme actuel vs objectif FIRE
- Identifier les mois de forte hausse/baisse et leur cause probable (contexte marché, DCA important)

```
📈 RYTHME D'ACCUMULATION MOYEN : +X XXX €/mois (derniers 12 mois)

À ce rythme sur [horizon restant] ans → patrimoine projeté : ~X XXX XXX €
Objectif FIRE (règle 4%) :                                    X XXX XXX €
[✅ Trajectoire favorable] OU [⚠️ Accélérer le DCA de X XXX €/mois]
```

---

### 9. Actions prioritaires

Termine par 3 actions concrètes et priorisées :

```
✅ ACTIONS PRIORITAIRES

1. [Action urgente — ex: "Abonder le PEA de X XXX € ce mois-ci (règle des 100−âge : vous devriez être à X%+ en actions)"]
2. [Action moyen terme — ex: "Ouvrir un PER et verser X XXX € avant le 31/12 → économie IR : X XXX €"]
3. [Action long terme — ex: "Prochaine SCPI en nue-propriété via AV pour optimiser la fiscalité"]

→ Lancez /rebalancing:SKILL pour savoir comment allouer votre DCA de X XXX €/mois.
```
