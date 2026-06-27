#!/usr/bin/env python3
"""
CGP Snapshot — Sauvegarde automatique de l'historique patrimonial.

Modes :
  python3 cgp/snapshot.py           → snapshot forcé du mois en cours
  python3 cgp/snapshot.py --auto    → snapshot seulement si patrimoine.json modifié
                                       (appelé par le hook Claude Code)
  python3 cgp/snapshot.py --month 2026-05  → snapshot pour un mois précis
  python3 cgp/snapshot.py --list    → liste les snapshots existants
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE    = PROJECT_ROOT / "data" / "patrimoine.json"
HISTORY_DIR  = PROJECT_ROOT / "data" / "history"


# ─── Wealth computations (miroir de cgp/export.py) ──────────────────────────

def compute(data: dict) -> dict:
    sit = data["situation_actuelle"]

    rp = sit["immobilier"]["residence_principale"]
    qp = rp["quote_part_pourcent"] / 100
    immo   = rp["valeur_brute"] * qp + sum(b.get("valeur", 0) for b in sit["immobilier"].get("locatif", []))
    passif = rp["capital_restant_du"] * qp + sum(b.get("capital_restant_du", 0) for b in sit["immobilier"].get("locatif", []))

    pea     = (sit.get("pea") or {}).get("valeur_actuelle", 0)
    pea_pme = (sit.get("pea_pme") or {}).get("valeur_actuelle", 0)
    cto     = (sit.get("cto") or {}).get("valeur_actuelle", 0)
    per     = (sit.get("per") or {}).get("valeur_actuelle", 0)
    av      = sum(c.get("valeur_totale", 0) for c in (sit.get("assurance_vie") or []))

    scpi_data  = sit.get("scpi") or {}
    pp_direct  = (scpi_data.get("pleine_propriete") or {}).get("en_direct") or {}
    scpi_np    = (scpi_data.get("nue_propriete") or {}).get("valeur_totale_np", 0)
    scpi_legacy = (scpi_data.get("en_direct") or {}).get("valeur_totale", 0)
    scpi       = pp_direct.get("valeur_totale", scpi_legacy) + scpi_np

    or_val  = (sit.get("or_physique") or {}).get("valeur_totale_eur", 0)
    pe_val  = (sit.get("private_equity") or {}).get("valeur_totale_eur", 0)
    crypto  = (sit.get("crypto") or {}).get("valeur_totale_eur", 0)

    liq_data = sit.get("liquidites") or {}
    liq = (
        (liq_data.get("livret_a") or {}).get("montant", 0) +
        (liq_data.get("ldds") or {}).get("montant", 0) +
        (liq_data.get("lep") or {}).get("montant", 0) +
        liq_data.get("compte_courant", 0)
    )

    assets = {
        "immobilier":         immo,
        "actions_pea":        pea + pea_pme + cto,
        "per":                per,
        "assurance_vie":      av,
        "scpi":               scpi,
        "or_physique":        or_val,
        "private_equity":     pe_val,
        "crypto":             crypto,
        "livrets_liquidites": liq,
    }
    gross = sum(assets.values())
    return {
        "assets": assets,
        "gross": gross,
        "net": gross - passif,
        "passif": passif,
    }


def pv_latentes(data: dict) -> dict:
    sit = data["situation_actuelle"]
    pv = {}

    pea = sit.get("pea") or {}
    if pea.get("valeur_actuelle") and pea.get("versements_cumules"):
        pv["pea"] = pea["valeur_actuelle"] - pea["versements_cumules"]

    crypto_positions = (sit.get("crypto") or {}).get("positions") or {}
    total_pv_crypto = 0
    for ticker, pos in crypto_positions.items():
        if isinstance(pos, dict) and pos.get("plus_value_latente_eur"):
            total_pv_crypto += pos["plus_value_latente_eur"]
    if total_pv_crypto:
        pv["crypto"] = total_pv_crypto

    or_data = sit.get("or_physique") or {}
    or_pv = 0
    for piece in or_data.get("pieces") or []:
        nb  = piece.get("nombre", 0)
        cur = piece.get("valeur_spot_unitaire_eur", 0)
        acq = piece.get("prix_acquisition_moyen_unitaire", 0)
        or_pv += nb * (cur - acq)
    for lingot in or_data.get("lingots") or []:
        or_pv += lingot.get("valeur_spot_eur", 0) - lingot.get("prix_acquisition_eur", 0)
    if or_pv:
        pv["or_physique"] = or_pv

    return pv


# ─── Snapshot I/O ────────────────────────────────────────────────────────────

def make_snapshot(data: dict, month: str, date_str: str) -> dict:
    vals = compute(data)
    return {
        "date":            date_str,
        "mois":            month,
        "patrimoine_brut": round(vals["gross"]),
        "patrimoine_net":  round(vals["net"]),
        "passif_total":    round(vals["passif"]),
        "dca_mensuel":     data["profil_investisseur"].get("dca_mensuel_cible", 0),
        "assets":          {k: round(v) for k, v in vals["assets"].items()},
        "allocation_pct":  {
            k: round(v / vals["gross"] * 100, 1) if vals["gross"] > 0 else 0
            for k, v in vals["assets"].items()
        },
        "pv_latentes": {k: round(v) for k, v in pv_latentes(data).items()},
    }


def save_snapshot(snap: dict, month: str) -> Path:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    out = HISTORY_DIR / f"{month}.json"
    out.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def load_latest_snapshot() -> dict | None:
    files = sorted(HISTORY_DIR.glob("*.json"))
    if not files:
        return None
    return json.loads(files[-1].read_text(encoding="utf-8"))


def has_significant_change(new: dict, existing: dict, threshold: int = 100) -> bool:
    """Returns True if gross wealth changed by more than threshold €."""
    return abs(new["patrimoine_brut"] - existing.get("patrimoine_brut", 0)) > threshold


# ─── CLI ─────────────────────────────────────────────────────────────────────

def cmd_snapshot(month: str, date_str: str, force: bool = False) -> None:
    if not DATA_FILE.exists():
        return  # Silently exit if no patrimoine.json (normal during first run)

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    snap = make_snapshot(data, month, date_str)

    out_file = HISTORY_DIR / f"{month}.json"
    if out_file.exists() and not force:
        existing = json.loads(out_file.read_text(encoding="utf-8"))
        if not has_significant_change(snap, existing):
            return  # No significant change → skip silently in auto mode

    path = save_snapshot(snap, month)
    print(f"📸 Snapshot sauvegardé → {path.relative_to(PROJECT_ROOT)}")
    print(f"   Brut : {snap['patrimoine_brut']:,} €  |  Net : {snap['patrimoine_net']:,} €".replace(",", " "))


def cmd_list() -> None:
    files = sorted(HISTORY_DIR.glob("*.json"))
    if not files:
        print("Aucun snapshot disponible. Lancez : python3 cgp/snapshot.py")
        return

    print(f"\n📅 HISTORIQUE PATRIMONIAL ({len(files)} snapshots)\n")
    print(f"  {'Mois':<10}  {'Brut':>14}  {'Net':>14}  {'Δ Brut':>12}")
    print(f"  {'─'*10}  {'─'*14}  {'─'*14}  {'─'*12}")

    prev_brut = None
    for f in files:
        snap = json.loads(f.read_text(encoding="utf-8"))
        brut = snap["patrimoine_brut"]
        net  = snap["patrimoine_net"]
        if prev_brut is not None:
            delta = brut - prev_brut
            sign  = "+" if delta >= 0 else ""
            delta_str = f"{sign}{delta:,}".replace(",", " ") + " €"
        else:
            delta_str = "    —"
        print(f"  {snap['mois']:<10}  {brut:>12,} €  {net:>12,} €  {delta_str:>12}".replace(",", " "))
        prev_brut = brut


def main() -> None:
    parser = argparse.ArgumentParser(description="CGP Snapshot — historique mensuel")
    parser.add_argument("--auto",  action="store_true", help="Mode hook : snapshot si changement significatif")
    parser.add_argument("--force", action="store_true", help="Forcer le snapshot même si inchangé")
    parser.add_argument("--month", default=None,        help="Mois cible (format YYYY-MM)")
    parser.add_argument("--list",  action="store_true", help="Lister les snapshots existants")
    args = parser.parse_args()

    if args.list:
        cmd_list()
        return

    now = datetime.now()
    month    = args.month or now.strftime("%Y-%m")
    date_str = now.strftime("%Y-%m-%d")

    if args.auto:
        cmd_snapshot(month, date_str, force=False)
    else:
        cmd_snapshot(month, date_str, force=args.force or True)


if __name__ == "__main__":
    main()
