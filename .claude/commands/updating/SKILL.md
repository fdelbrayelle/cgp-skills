# /updating:SKILL — Mise à Jour Sélective du Patrimoine

Lis `data/patrimoine.json` (outil Read). Affiche les valeurs actuelles et permets une mise à jour chirurgicale sans relancer l'onboarding complet.

## Argument optionnel

Si `$ARGUMENTS` est fourni (ex : `/updating:SKILL pea.valeur_actuelle`), pré-sélectionne ce champ directement.

---

## Menu de mise à jour

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

PEA
  [11] Valeur actuelle PEA             → XX XXX €
  [12] Versements cumulés PEA          → XX XXX €

PER
  [13] Valeur actuelle PER             → XX XXX €
  [14] Dont fonds euros / UC           → X XXX € / XX XXX €

ASSURANCE VIE
  [15] Mettre à jour un contrat AV     → (liste les contrats)

SCPI PP EN DIRECT
  [16] Valeur totale SCPI PP           → XX XXX €
  [17] Ajouter / modifier une SCPI PP  → (interactif)
  [18] Réinvestissement des loyers     → oui/non par SCPI

SCPI NUE-PROPRIÉTÉ
  [19] Valeur totale NP                → XX XXX €
  [20] Ajouter / modifier une SCPI NP  → (interactif)

OR PHYSIQUE
  [21] Valeur totale or                → XX XXX €
  [22] Mettre à jour le prix spot      → (recalcule depuis quantités)
  [23] Ajouter pièces / lingots        → (interactif)

PRIVATE EQUITY
  [24] Valeur liquidative estimée      → X XXX €
  [25] Ajouter un fonds               → (interactif)

CRYPTO
  [26] Valeur totale crypto            → XX XXX €
  [27] Mettre à jour une position      → (sélection par ticker)
  [28] Ajouter / supprimer une crypto  → (interactif)

IMMOBILIER
  [29] Valeur résidence principale     → XXX XXX €
  [30] Quote-part résidence (%)        → XX%
  [31] Capital restant dû              → XXX XXX €

BSPCE *(si présents)*
  [32] Valeur action estimée           → X,XX €/action (recalcule la PV latente)
  [33] Ajouter une tranche BSPCE       → (interactif)
  [34] Marquer des BSPCE comme exercés → (sélection par entreprise)

  [0]  Ajouter un champ non listé

Tapez le numéro du champ à mettre à jour :
```

## Processus

1. Affiche valeur actuelle
2. Demande nouvelle valeur (formats acceptés : `45000`, `45 000`, `45 000€`)
3. Confirmation avant sauvegarde
4. Met à jour `date_mise_a_jour` avec la date du jour
5. Sauvegarde avec l'outil Write
6. Affiche l'impact sur patrimoine brut/net si significatif

## Cas spéciaux

**Mise à jour valeur action BSPCE [32]** :
- Affiche chaque tranche avec l'entreprise, le prix d'exercice et la valeur action actuelle
- Demande le nouveau prix de l'action (dernière valorisation connue)
- Recalcule automatiquement `plus_value_latente_estimee_eur` = (valeur_action − prix_exercice) × nombre_bspce

**Mise à jour du prix spot de l'or [22]** :
- Affiche chaque type de pièce/lingot avec leur quantité
- Demande le nouveau prix spot par gramme ou par pièce
- Recalcule automatiquement `valeur_totale_eur`

**Réinvestissement des loyers SCPI [18]** :
- Si activé : expliquer que la valeur totale augmente automatiquement → mettre à jour `valeur_part_actuelle` × `nombre_parts`

**Crypto [27]** :
- Sélectionner le ticker
- Mettre à jour : quantite, valeur_eur, prix_moyen_acquisition (si DCA supplémentaire)

## Après la sauvegarde

```
✅ Mis à jour. Nouveau patrimoine brut : XXX XXX € (Δ : +/−X XXX €)

→ /auditing:SKILL   pour voir l'audit complet
→ /rebalancing:SKILL pour recalculer le DCA de ce mois
```
