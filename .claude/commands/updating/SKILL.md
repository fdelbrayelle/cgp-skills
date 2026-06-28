# /updating:SKILL — Mise à Jour Sélective du Patrimoine

Lis `data/patrimoine.json` (outil Read). Affiche les valeurs actuelles et permets une mise à jour chirurgicale sans relancer l'onboarding complet.

## Argument optionnel

Si `$ARGUMENTS` est fourni (ex : `/updating:SKILL pea.valeur_actuelle`), pré-sélectionne ce champ directement.

---

## Menu principal

```
🔧 MISE À JOUR PATRIMONIALE — [prenom_nom]
   Dernière mise à jour : [date]

PROFIL
  [1]  DCA mensuel cible               → X XXX €/mois
  [2]  Dépenses mensuelles courantes   → X XXX €/mois
  [3]  Profil de risque                → [profil]
  [4]  Horizon d'investissement        → [horizon] ans
  [5]  Objectif revenu mensuel passif  → X XXX €/mois

ALLOCATION CIBLE
  [6]  Toute l'allocation cible        → (re-saisie complète)

LIQUIDITÉS
  [7]  Livret A                        → XX XXX €
  [8]  LDDS                            → XX XXX €
  [9]  LEP                             → XX XXX €
  [10] Compte courant                  → X XXX €

ENVELOPPES FINANCIÈRES
  [11] PEA / PEA-PME / CTO            → [N] enveloppe(s) — XX XXX € au total
  [12] PER                             → XX XXX €
  [13] Assurance Vie                   → [N] contrat(s) — XX XXX € au total
  [14] SCPI                            → XX XXX € (PP + NP)
  [15] Or physique                     → XX XXX €
  [16] Private Equity                  → XX XXX €
  [17] Crypto                          → XX XXX €
  [18] BSPCE                           → [N] tranche(s) (si applicable)

IMMOBILIER
  [19] Valeur résidence principale     → XXX XXX €
  [20] Quote-part résidence (%)        → XX%
  [21] Capital restant dû              → XXX XXX €

  [0]  Ajouter un champ non listé

Tapez le numéro du champ à mettre à jour :
```

---

## Processus général (champs simples)

1. Affiche valeur actuelle
2. Demande nouvelle valeur (formats acceptés : `45000`, `45 000`, `45 000€`)
3. Confirmation avant sauvegarde
4. Met à jour `date_mise_a_jour` avec la date du jour
5. Sauvegarde avec l'outil Write
6. Affiche l'impact sur patrimoine brut/net si significatif

---

## Flux interactif enveloppes [11–18]

Pour chaque catégorie, le processus est identique en 3 temps :

### Temps 1 — Affichage des enveloppes existantes

Lire `patrimoine.json` et afficher toutes les enveloppes de la catégorie avec leurs valeurs clés. Afficher le DCA programmé sur la même ligne si non null.

**Exemple pour l'Assurance Vie [13] :**
```
📋 Assurance Vie — 3 contrats

  [1] Linxea Spirit 2 (Spirica)  — ouvert 2018 — 45 200 € (fonds € 20k / UC 25,2k) — 🔄 300 €/mois
  [2] Boursorama Vie (Generali)  — ouvert 2021 — 12 800 € (fonds € 12k / UC 0,8k)  — 🔄 non programmé
  [3] Carac (Carac)              — ouvert 2015 — 8 500 €  (fonds € 8,5k / UC 0)     — 🔄 non programmé

  [A] Ajouter un nouveau contrat AV
  [0] Annuler

Sélectionnez une enveloppe ou [A] pour en ajouter une nouvelle :
```

### Temps 2 — Mise à jour d'une enveloppe existante

Une fois l'enveloppe sélectionnée, afficher ses champs éditables et demander lequel mettre à jour :

```
📝 Linxea Spirit 2 — Champs modifiables

  [a] Fonds euros                    → 20 000 €
  [b] Unités de compte (UC)         → 25 200 €
  [c] Valeur totale                  → 45 200 €
  [d] Versements cumulés             → 38 000 €
  [e] SCPI logées dans ce contrat   → 5 000 €
  [f] DCA mensuel programmé          → 300 €/mois  (null = géré par drift)

Quel champ mettre à jour ?
```

Après saisie, recalculer `valeur_totale` si fonds_euros ou UC sont modifiés séparément.

**Pour le champ [f] DCA mensuel programmé :**
- Accepter une valeur en € (ex : `300`, `300€`, `300 €/mois`) ou `0` / `aucun` pour remettre à `null`
- Afficher après saisie : *"DCA programmé mis à jour. Total programmé toutes enveloppes : X XXX €/mois sur X XXX € de DCA cible."*
- Si total programmé > dca_mensuel_cible → avertir : *"⚠️ Le total des DCA programmés (X XXX €) dépasse votre DCA mensuel cible (X XXX €)."*

### Temps 3 — Ajout d'une nouvelle enveloppe [A]

Lancer le mini-onboarding correspondant (voir section ci-dessous). Une seule question à la fois, attendre la réponse avant de continuer.

---

## Mini-onboardings par type d'enveloppe

### [11] PEA / PEA-PME / CTO

```
Quel type d'enveloppe souhaitez-vous ajouter ?
  [a] PEA (Plan d'Épargne en Actions)
  [b] PEA-PME
  [c] CTO (Compte-Titres Ordinaire)
```

**PEA** : broker → date d'ouverture (AAAA-MM-JJ, importante pour l'exonération 5 ans) → valeur actuelle → versements cumulés → **DCA mensuel programmé** (€/mois ou `aucun`).

**PEA-PME** : broker → valeur actuelle → **DCA mensuel programmé** (€/mois ou `aucun`).

**CTO** : broker → valeur actuelle → **DCA mensuel programmé** (€/mois ou `aucun`).

### [12] PER

```
Quel type de PER ?
  [a] Individuel (PERIN) — ex : Linxea Spirit PER, Yomoni Retraite
  [b] Collectif employeur (PERCOL)
  [c] Catégoriel (PERCAT / article 83)
```

Questions : assureur/gestionnaire → valeur actuelle → dont fonds euros → dont UC → versements prévus cette année → **DCA mensuel programmé** (€/mois ou `aucun`).

### [13] Assurance Vie

Questions : nom du contrat → assureur → date d'ouverture (AAAA-MM-JJ) → montant fonds euros → montant UC → valeur totale → versements cumulés → **DCA mensuel programmé** (€/mois ou `aucun`).

Demander ensuite : *"Des SCPI sont-elles logées dans ce contrat ? Si oui, quel montant ? (sera inclus dans la valeur totale, non recompté en SCPI directe)"*

### [14] SCPI

```
Quel type de SCPI ?
  [a] Pleine propriété en direct
  [b] Via Assurance Vie (sera rattachée à un contrat existant)
  [c] Nue-propriété
```

**PP en direct** : nom de la SCPI → nombre de parts → prix d'acquisition par part (€) → valeur actuelle par part (€) → rendement estimé (%) → loyers annuels bruts estimés (€) → réinvestissement des loyers activé ? (oui/non) → date de première acquisition → **DCA mensuel programmé** (€/mois ou `aucun` — ticket élevé, souvent accumulation).

**Via AV** : quel contrat AV ? → montant. Rappeler que ce montant est déjà inclus dans la valeur totale de l'AV.

**Nue-propriété** : nom → nombre de parts → prix d'achat NP par part (€) → valeur PP estimée par part (€) → décote NP (%) → date d'achat → date de fin d'usufruit.

### [15] Or physique

```
Que souhaitez-vous ajouter ?
  [a] Pièces
  [b] Lingot
```

**Pièces** : type (Napoléon 20F, Souverain, Krugerrand, Vreneli…) → nombre → valeur spot actuelle par pièce (€) → prix d'acquisition moyen par pièce (€) → lieu de stockage.

**Lingot** : poids en grammes → valeur spot actuelle (€) → prix d'acquisition (€) → lieu de stockage.

Recalculer `valeur_totale_eur` après ajout.

### [16] Private Equity

```
Quel type de véhicule ?
  [a] FCPI
  [b] FIP
  [c] Fonds professionnel (FPCI/FCPR)
  [d] Club deal
  [e] Investissement direct
```

**FCPI/FIP** : nom → gestionnaire → vintage (année de souscription) → montant souscrit (€) → dernière valeur liquidative estimée (€) → réduction IR obtenue (€ et %) → date de fin de blocage estimée.

Recalculer `valeur_totale_eur` après ajout.

### [17] Crypto

Questions : ticker (ex : BTC, ETH, SOL) → quantité détenue → valeur actuelle en € → prix moyen d'acquisition par unité (€) — crucial pour le calcul de PV — → lieu de stockage (exchange ou cold wallet).

Calculer automatiquement : `cout_acquisition_total_eur = quantite × prix_moyen` et `plus_value_latente_eur = valeur_eur − cout_acquisition_total_eur`.

Demander si des positions DeFi/staking sont associées : protocole → valeur (€) → rendement annuel estimé (%).

Demander ensuite : **DCA mensuel programmé** sur la crypto totale (€/mois ou `aucun`).

Rappeler l'obligation de déclarer les exchanges étrangers (formulaire 3916-bis).

Recalculer `valeur_totale_eur` après ajout.

### [18] BSPCE

Demander d'abord : *"Dans quelle entreprise avez-vous reçu ces BSPCE ?"*

Questions : date d'attribution (AAAA-MM-JJ) → nombre de BSPCE → prix d'exercice (€/action) → vesting cliff (mois) → date de fin de vesting → déjà exercés ? (oui/non, si oui combien ?) → valeur estimée de l'action aujourd'hui (€ ou "inconnue") → **âge de l'entreprise à la date d'attribution** (années — clé fiscale : < 3 ans → PFU 30%, ≥ 3 ans → 17,2% PS uniquement).

Calculer `plus_value_latente_estimee_eur = (valeur_action − prix_exercice) × (nombre_bspce − nombre_exerces)`.

---

## Cas spéciaux supplémentaires

**DCA mensuel cible [1]** :
- Demander uniquement la nouvelle valeur en € (ex : `1500`, `1 500`, `1 500€`)
- ⚠️ NE PAS demander de pourcentage — ce n'est pas une allocation cible

**Mise à jour valeur action BSPCE (via [18])** :
- Afficher chaque tranche avec l'entreprise, le prix d'exercice et la valeur action actuelle
- Demander le nouveau prix de l'action (dernière valorisation connue)
- Recalculer `plus_value_latente_estimee_eur` automatiquement

**Mise à jour du prix spot de l'or (via [15])** :
- Afficher chaque type de pièce/lingot avec leur quantité
- Demander le nouveau prix spot par gramme ou par pièce
- Recalculer automatiquement `valeur_totale_eur`

**SCPI — réinvestissement des loyers (via [14])** :
- Si activé : expliquer que la valeur totale augmente automatiquement → mettre à jour `valeur_part_actuelle` × `nombre_parts`

**Crypto — mise à jour position existante (via [17])** :
- Sélectionner le ticker
- Mettre à jour : quantite, valeur_eur, prix_moyen_acquisition (si DCA supplémentaire)

---

## Après la sauvegarde

```
✅ Mis à jour. Nouveau patrimoine brut : XXX XXX € (Δ : +/−X XXX €)

→ /auditing:SKILL    pour voir l'audit complet
→ /rebalancing:SKILL pour recalculer le DCA de ce mois
```
