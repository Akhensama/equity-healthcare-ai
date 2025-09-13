# app/reporting/run_demo.py

import argparse
from datetime import date, timedelta
import os
import pandas as pd

from app.reporting.compute_metrics import compute_report_metrics
from app.reporting.generate_equity_report import generate_equity_report


# ---------- Helpers ----------

def _fmt_yes_no(v=True):
    return "Yes" if v else "No"


def _derive_mitigation_status(after: dict) -> str:
    """
    If compute_report_metrics already gives a status (same logic as baseline),
    prefer that. Otherwise derive from gaps with simple thresholds.
    """
    if not after:
        return "FAIL"
    if "baseline_status" in after and after["baseline_status"] in ("✅", "⚠", "PASS", "FAIL"):
        return after["baseline_status"]

    try:
        gap_auroc = float(after.get("gap_auroc", "nan"))
        gap_fnr = float(after.get("gap_fnr", "nan"))
        calib_gap = float(after.get("calib_gap", "nan"))
        ok = (
            pd.notna(gap_auroc) and abs(gap_auroc) <= 2
            and pd.notna(gap_fnr) and abs(gap_fnr) <= 5
            and pd.notna(calib_gap) and calib_gap <= 0.05
        )
        return "PASS" if ok else "FAIL"
    except Exception:
        return "FAIL"


def _build_recommendation(base: dict, after: dict | None) -> str:
    if not after:
        return "Baseline computed. Mitigation not yet applied."

    parts = []
    try:
        g_before = base.get("gap_fnr")
        g_after = after.get("gap_fnr")
        if pd.notna(g_before) and pd.notna(g_after):
            delta = float(g_before) - float(g_after)
            direction = "down" if delta > 0 else "up"
            parts.append(
                f"FNR gap {g_before} pp -> {g_after} pp "
                f"({direction} by {abs(delta):.1f} pp)"
            )
    except Exception:
        pass

    try:
        auroc_b = base.get("gap_auroc")
        auroc_a = after.get("gap_auroc")
        if pd.notna(auroc_b) and pd.notna(auroc_a):
            parts.append(f"AUROC gap {auroc_b} pp -> {auroc_a} pp")
    except Exception:
        pass

    if parts:
        return " ; ".join(parts) + ". Recommend sandbox evaluation with clinical review."
    return "Mitigation applied. Recommend sandbox evaluation with clinical review."



def to_ascii_flag(x: str | None) -> str:
    """Map Unicode/emoji/checkmarks to plain ASCII words."""
    if not x:
        return "FAIL"
    x = str(x).strip()
    return "PASS" if x in ("✅", "PASS", "OK", "Yes", "True") else "FAIL"


def normalize_flags(report: dict) -> None:
    """Normalize all status/flag fields in-place before rendering."""
    for k in [
        "representation_status",
        "baseline_status",
        "mitigation_status",
        "privacy_status",
        "utility_flag",
        "fairness_flag",
        "privacy_flag",
        "privacy_pass",
        "mia_pass",
    ]:
        if k in report:
            report[k] = to_ascii_flag(report[k])


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(
        description="Generate BEFORE/AFTER equity report using the Markdown template."
    )
    ap.add_argument("--csv_before", required=True, help="Path to BEFORE (original/imbalanced) CSV")
    ap.add_argument("--csv_after", required=False, help="Path to AFTER (synthetic balanced) CSV")
    ap.add_argument("--out", required=True, help="Path to write the Markdown report")
    ap.add_argument("--thr", type=float, default=0.5, help="Decision threshold for FNR/FPR (default 0.5)")
    ap.add_argument("--hospital", default="Demo General Hospital", help="Hospital name")
    args = ap.parse_args()

    # ---------- Load BEFORE ----------
    df_before = pd.read_csv(args.csv_before)
    base = compute_report_metrics(
        df_before, score_col="score", label_col="label", sex_col="sex", thr=args.thr
    )

    # ---------- Load AFTER (optional) ----------
    after = None
    if args.csv_after:
        df_after = pd.read_csv(args.csv_after)
        after = compute_report_metrics(
            df_after, score_col="score", label_col="label", sex_col="sex", thr=args.thr
        )

    # ---------- Assemble fields for template ----------
    today = date.today()
    report = {}

    # Static/governance/meta
    report.update(
        {
            "hospital_name": args.hospital,
            "date": today.isoformat(),
            "next_review_date": (today + timedelta(days=180)).isoformat(),
            "yes_no": _fmt_yes_no(True),
            "version": "v0.1",
        }
    )

    # BEFORE (baseline) — copy everything compute_report_metrics provides
    report.update(base)

    # Detect method (temporary heuristic)
    if args.csv_after and "smote" in args.csv_after.lower():
        method_used = "SMOTE oversampling"
    elif args.csv_after and "ctgan" in args.csv_after.lower():
        method_used = "CTGAN female oversampling"
    else:
        method_used = "Unknown mitigation"
        
    # AFTER (mitigation) — map to _syn fields expected by the template
    if after:
        report.update(
            {
                "method_name": method_used,
                "pct_female_syn": after.get("pct_female", "N/A"),
                "auroc_m_syn": after.get("auroc_m", "N/A"),
                "auroc_f_syn": after.get("auroc_f", "N/A"),
                "gap_auroc_syn": after.get("gap_auroc", "N/A"),
                "fnr_m_syn": after.get("fnr_m", "N/A"),
                "fnr_f_syn": after.get("fnr_f", "N/A"),
                "gap_fnr_syn": after.get("gap_fnr", "N/A"),
                "calib_gap_syn": after.get("calib_gap", "N/A"),
                "mitigation_status": _derive_mitigation_status(after),
            }
        )
    else:
        report.update(
            {
                "method_name": "N/A",
                "pct_female_syn": "N/A",
                "auroc_m_syn": "N/A",
                "auroc_f_syn": "N/A",
                "gap_auroc_syn": "N/A",
                "fnr_m_syn": "N/A",
                "fnr_f_syn": "N/A",
                "gap_fnr_syn": "N/A",
                "calib_gap_syn": "N/A",
                "mitigation_status": "FAIL",
            }
        )

    # Privacy/utility placeholders
    report.update(
        {
            "nn_distance": "N/A",
            "privacy_pass": "FAIL",
            "mia_auc": "N/A",
            "mia_pass": "FAIL",
            "utility_drop": "N/A",
            "privacy_status": "FAIL",
        }
    )

    # Overall verdict flags
    report["utility_flag"] = "PASS" if report.get("baseline_status") == "PASS" else "FAIL"
    report["fairness_flag"] = (
        "PASS"
        if (report.get("baseline_status") == "PASS" and report.get("mitigation_status", "FAIL") == "PASS")
        else "FAIL"
    )
    report["privacy_flag"] = report.get("privacy_status", "FAIL")

    # Recommendation text
    report["recommendation_text"] = _build_recommendation(base, after)

    # Normalize all PASS/FAIL style fields
    normalize_flags(report)

    # ---------- Render to Markdown ----------
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out_path = generate_equity_report(report, args.out)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
