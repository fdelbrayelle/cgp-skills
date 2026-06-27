#!/usr/bin/env python3
"""
CGP Export — Génération de rapports patrimoniaux HTML / PDF / PNG.

Usage:
    python cgp/export.py [--format html|pdf|png] [--scope global|financial|dca]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "patrimoine.json"
EXPORTS_DIR = Path(__file__).parent.parent / "exports"

LABELS = {
    "immobilier":         "Immobilier",
    "actions_pea":        "Actions / PEA",
    "per":                "Épargne Retraite (PER)",
    "assurance_vie":      "Assurance Vie",
    "scpi":               "SCPI",
    "or_physique":        "Or physique",
    "private_equity":     "Private Equity",
    "crypto":             "Crypto",
    "livrets_liquidites": "Livrets & Liquidités",
}

COLORS = {
    "immobilier":         "#3b82f6",
    "actions_pea":        "#10b981",
    "per":                "#f59e0b",
    "assurance_vie":      "#8b5cf6",
    "scpi":               "#ec4899",
    "or_physique":        "#d97706",
    "private_equity":     "#7c3aed",
    "crypto":             "#f97316",
    "livrets_liquidites": "#6b7280",
}


# ─── Data loading ────────────────────────────────────────────────────────────

def load() -> dict:
    if not DATA_FILE.exists():
        print(f"Erreur : {DATA_FILE} introuvable. Exécutez /initializing d'abord.", file=sys.stderr)
        sys.exit(1)
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


# ─── Wealth computations ─────────────────────────────────────────────────────

def compute(data: dict) -> dict:
    """Compute all wealth metrics from patrimoine data."""
    sit = data["situation_actuelle"]

    rp = sit["immobilier"]["residence_principale"]
    qp = rp["quote_part_pourcent"] / 100
    immo = rp["valeur_brute"] * qp + sum(
        b.get("valeur", 0) for b in sit["immobilier"].get("locatif", [])
    )
    passif = rp["capital_restant_du"] * qp + sum(
        b.get("capital_restant_du", 0) for b in sit["immobilier"].get("locatif", [])
    )

    pea     = (sit.get("pea") or {}).get("valeur_actuelle", 0)
    pea_pme = (sit.get("pea_pme") or {}).get("valeur_actuelle", 0)
    cto     = (sit.get("cto") or {}).get("valeur_actuelle", 0)

    per = (sit.get("per") or {}).get("valeur_actuelle", 0)
    av  = sum(c.get("valeur_totale", 0) for c in (sit.get("assurance_vie") or []))

    # SCPI — PP en direct + NP (ne pas compter via AV, déjà dans av_total)
    scpi_data = sit.get("scpi") or {}
    pp_direct = (scpi_data.get("pleine_propriete") or {}).get("en_direct") or {}
    scpi_np   = (scpi_data.get("nue_propriete") or {}).get("valeur_totale_np", 0)
    # Fallback pour ancienne structure sans PP/NP
    scpi_legacy = (scpi_data.get("en_direct") or {}).get("valeur_totale", 0)
    scpi = pp_direct.get("valeur_totale", scpi_legacy) + scpi_np

    or_data = sit.get("or_physique") or {}
    or_val  = or_data.get("valeur_totale_eur", 0)

    pe_data = sit.get("private_equity") or {}
    pe_val  = pe_data.get("valeur_totale_eur", 0)

    crypto = (sit.get("crypto") or {}).get("valeur_totale_eur", 0)

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


def alloc_pct(assets: dict, gross: float) -> dict:
    if gross == 0:
        return {k: 0.0 for k in assets}
    return {k: v / gross * 100 for k, v in assets.items()}


def drift(current: dict, target: dict) -> dict:
    return {k: current.get(k, 0) - target.get(k, 0) for k in target}


def dca_split(drft: dict, monthly: float) -> dict:
    lagging = {k: abs(v) for k, v in drft.items() if v < 0}
    if not lagging:
        return {}
    total = sum(lagging.values())
    return {k: v / total * monthly for k, v in lagging.items()}


# ─── SVG generation ──────────────────────────────────────────────────────────

def _fmt(v: float) -> str:
    return f"{v:,.0f} €".replace(",", " ")


def svg_bars(items: dict, ref: float, title: str = "", width: int = 560) -> str:
    """Horizontal bar chart as inline SVG."""
    lw, cw, bh, gap, pad = 165, 280, 26, 10, 30
    entries = list(items.items())
    h = pad + len(entries) * (bh + gap) + 10

    bars = ""
    for i, (k, v) in enumerate(entries):
        y   = pad + i * (bh + gap)
        bw  = (v / ref * cw) if ref > 0 else 0
        col = COLORS.get(k, "#6b7280")
        lbl = LABELS.get(k, k)
        val = _fmt(v) if v >= 1 else f"{v:.1f}%"
        bars += (
            f'<text x="{lw-6}" y="{y+19}" text-anchor="end" '
            f'font-size="12" fill="#374151">{lbl}</text>'
            f'<rect x="{lw}" y="{y}" width="{bw:.1f}" height="{bh}" '
            f'fill="{col}" rx="4" opacity="0.85"/>'
            f'<text x="{lw+bw+6}" y="{y+19}" font-size="12" fill="#374151">{val}</text>'
        )

    title_el = (
        f'<text x="{width//2}" y="18" text-anchor="middle" '
        f'font-size="13" font-weight="bold" fill="#1f2937">{title}</text>'
        if title else ""
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}">'
        f'<style>text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}</style>'
        f'{title_el}{bars}</svg>'
    )


def svg_alloc_vs_target(assets: dict, gross: float, target: dict) -> str:
    """Dual-bar chart: current vs target allocation."""
    lw, cw, bh, gap, pad = 165, 260, 20, 16, 30
    entries = list(target.keys())
    curr = alloc_pct(assets, gross)
    h = pad + len(entries) * (bh * 2 + gap) + 10

    bars = ""
    for i, k in enumerate(entries):
        y    = pad + i * (bh * 2 + gap)
        c    = curr.get(k, 0)
        t    = target.get(k, 0)
        col  = COLORS.get(k, "#6b7280")
        lbl  = LABELS.get(k, k)
        d    = c - t
        dc   = "#ef4444" if d < -2 else "#10b981" if d > 2 else "#f59e0b"
        bw_c = c / 100 * cw
        bw_t = t / 100 * cw
        bars += (
            f'<text x="{lw-6}" y="{y+15}" text-anchor="end" font-size="11" fill="#374151">{lbl}</text>'
            f'<rect x="{lw}" y="{y}" width="{bw_c:.1f}" height="{bh}" fill="{col}" rx="3" opacity="0.85"/>'
            f'<text x="{lw+bw_c+4}" y="{y+15}" font-size="11" fill="#374151">{c:.1f}%</text>'
            f'<rect x="{lw}" y="{y+bh+3}" width="{bw_t:.1f}" height="{bh-6}" fill="{col}" rx="3" opacity="0.25"/>'
            f'<text x="{lw+bw_t+4}" y="{y+bh+16}" font-size="10" fill="#9ca3af">{t:.1f}% cible</text>'
            f'<text x="{lw+cw+12}" y="{y+15}" font-size="11" fill="{dc}" font-weight="bold">{d:+.1f}%</text>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{lw+cw+80}" height="{h}">'
        f'<style>text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}</style>'
        f'<text x="{(lw+cw+80)//2}" y="18" text-anchor="middle" font-size="13" '
        f'font-weight="bold" fill="#1f2937">Allocation Actuelle vs Cible</text>'
        f'{bars}</svg>'
    )


# ─── HTML report ─────────────────────────────────────────────────────────────

def generate_html(data: dict, scope: str = "global") -> str:
    vals   = compute(data)
    curr   = alloc_pct(vals["assets"], vals["gross"])
    target = data.get("allocation_cible", {})
    drft   = drift(curr, target)
    prof   = data["profil_investisseur"]
    dca_m  = prof.get("dca_mensuel_cible", 0)
    dca    = dca_split(drft, dca_m)
    now    = datetime.now().strftime("%d/%m/%Y à %H:%M")

    asset_svg  = svg_bars(vals["assets"], vals["gross"], "Répartition brute")
    alloc_svg  = svg_alloc_vs_target(vals["assets"], vals["gross"], target)

    def row(k: str, v: float) -> str:
        c  = curr.get(k, 0)
        t  = target.get(k, 0)
        d  = drft.get(k, 0)
        dc = "#ef4444" if d < -2 else "#10b981" if d > 2 else "#f59e0b"
        return (
            f'<tr><td>{LABELS.get(k,k)}</td>'
            f'<td style="text-align:right">{_fmt(v)}</td>'
            f'<td style="text-align:right">{c:.1f}%</td>'
            f'<td style="text-align:right">{t:.1f}%</td>'
            f'<td style="text-align:right;color:{dc};font-weight:600">{d:+.1f}%</td></tr>'
        )

    alloc_rows = "".join(row(k, v) for k, v in vals["assets"].items())

    if scope in ("global", "dca"):
        if dca:
            dca_rows = "".join(
                f'<tr><td>{LABELS.get(k,k)}</td>'
                f'<td style="text-align:right;color:#10b981;font-weight:600">{_fmt(v)}</td>'
                f'<td style="text-align:right">{v/dca_m*100:.1f}%</td></tr>'
                for k, v in dca.items()
            )
            dca_section = (
                f'<h2>Allocation DCA — {_fmt(dca_m)}/mois</h2>'
                f'<table><tr><th>Actif cible</th><th style="text-align:right">Montant</th>'
                f'<th style="text-align:right">% DCA</th></tr>{dca_rows}</table>'
            )
        else:
            dca_section = (
                '<h2>Allocation DCA</h2>'
                '<p style="color:#10b981;font-weight:600">✅ Portefeuille équilibré — '
                'aucun rééquilibrage requis ce mois-ci.</p>'
            )
    else:
        dca_section = ""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audit Patrimonial — {prof.get("prenom_nom","")}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
     background:#f3f4f6;color:#1f2937;padding:32px 16px}}
.wrap{{max-width:900px;margin:0 auto;background:#fff;border-radius:16px;
      box-shadow:0 4px 32px rgba(0,0,0,.10);padding:48px 40px}}
h1{{font-size:28px;color:#111827;margin-bottom:6px}}
.sub{{color:#6b7280;font-size:14px;margin-bottom:32px}}
h2{{font-size:17px;color:#374151;margin:32px 0 14px;
   border-bottom:2px solid #e5e7eb;padding-bottom:8px}}
.kpis{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:28px}}
.kpi{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:20px;text-align:center}}
.kpi .lbl{{font-size:11px;color:#6b7280;margin-bottom:8px;text-transform:uppercase;
          letter-spacing:.06em}}
.kpi .val{{font-size:22px;font-weight:700}}
.blue{{color:#3b82f6}}.green{{color:#10b981}}.red{{color:#ef4444}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin-bottom:12px}}
th{{background:#f3f4f6;padding:10px 14px;text-align:left;font-size:11px;
   text-transform:uppercase;letter-spacing:.05em;color:#6b7280}}
td{{padding:10px 14px;border-bottom:1px solid #f9fafb}}
tr:last-child td{{border-bottom:none}}
.chart{{margin:20px 0;background:#f9fafb;border:1px solid #e5e7eb;
       border-radius:10px;padding:20px;overflow-x:auto}}
.footer{{margin-top:40px;padding-top:18px;border-top:1px solid #e5e7eb;
        font-size:11px;color:#9ca3af;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}}
@media(max-width:600px){{.kpis{{grid-template-columns:1fr}}.wrap{{padding:24px 16px}}}}
</style>
</head>
<body>
<div class="wrap">
  <h1>Audit Patrimonial</h1>
  <p class="sub">
    {prof.get("prenom_nom","")} &nbsp;·&nbsp;
    Profil <strong>{prof.get("profil_risque","").title()}</strong> &nbsp;·&nbsp;
    {prof.get("age","?")} ans &nbsp;·&nbsp;
    Horizon {prof.get("horizon_annees","?")} ans &nbsp;·&nbsp;
    {now}
  </p>

  <div class="kpis">
    <div class="kpi"><div class="lbl">Patrimoine Brut</div>
      <div class="val blue">{_fmt(vals["gross"])}</div></div>
    <div class="kpi"><div class="lbl">Patrimoine Net</div>
      <div class="val green">{_fmt(vals["net"])}</div></div>
    <div class="kpi"><div class="lbl">Passif (crédits)</div>
      <div class="val red">{_fmt(vals["passif"])}</div></div>
  </div>

  <div class="chart">{asset_svg}</div>

  <h2>Allocation Actuelle vs Cible</h2>
  <div class="chart">{alloc_svg}</div>

  <table>
    <tr>
      <th>Classe d'actif</th>
      <th style="text-align:right">Valeur</th>
      <th style="text-align:right">Actuel %</th>
      <th style="text-align:right">Cible %</th>
      <th style="text-align:right">Écart</th>
    </tr>
    {alloc_rows}
  </table>

  {dca_section}

  <div class="footer">
    <span>CGP Skills · Usage strictement personnel</span>
    <span>Données locales non transmises · {DATA_FILE.name} non versionné</span>
  </div>
</div>
</body>
</html>"""


# ─── Entry point ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CGP Export — génère un rapport patrimonial HTML/PDF/PNG"
    )
    parser.add_argument(
        "--format", choices=["html", "pdf", "png"], default="html",
        help="Format de sortie (défaut : html)"
    )
    parser.add_argument(
        "--scope", choices=["global", "financial", "dca"], default="global",
        help="Périmètre du rapport (défaut : global)"
    )
    args = parser.parse_args()

    data = load()
    EXPORTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html  = generate_html(data, scope=args.scope)

    if args.format == "html":
        out = EXPORTS_DIR / f"audit_{args.scope}_{stamp}.html"
        out.write_text(html, encoding="utf-8")

    elif args.format == "pdf":
        try:
            import weasyprint  # type: ignore
        except ImportError:
            print(
                "Erreur : weasyprint non installé.\n"
                "  pip install weasyprint\n"
                "  (Ubuntu/Debian : sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0)",
                file=sys.stderr,
            )
            sys.exit(1)
        out = EXPORTS_DIR / f"audit_{args.scope}_{stamp}.pdf"
        weasyprint.HTML(string=html, base_url=str(EXPORTS_DIR)).write_pdf(str(out))

    elif args.format == "png":
        try:
            import cairosvg  # type: ignore
        except ImportError:
            print("Erreur : cairosvg non installé.\n  pip install cairosvg", file=sys.stderr)
            sys.exit(1)
        vals   = compute(data)
        target = data.get("allocation_cible", {})
        svg    = svg_alloc_vs_target(vals["assets"], vals["gross"], target)
        out    = EXPORTS_DIR / f"audit_{args.scope}_{stamp}.png"
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out), scale=2)

    print(f"✓ Rapport exporté : {out}")


if __name__ == "__main__":
    main()
