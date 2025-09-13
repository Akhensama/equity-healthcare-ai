# app/reporting/compute_metrics.py

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, brier_score_loss, confusion_matrix


# ---------- helpers ----------

def _safe_auroc(y_true: np.ndarray, y_score: np.ndarray) -> float | float("nan"):
    """AUROC if both classes are present; else NaN."""
    y_true = y_true.astype(int)
    # need at least one 0 and one 1
    if len(np.unique(y_true)) < 2:
        return float("nan")
    try:
        return float(roc_auc_score(y_true, y_score))
    except Exception:
        return float("nan")


def _fnr_at_threshold(y_true: np.ndarray, y_score: np.ndarray, thr: float) -> float:
    """
    False Negative Rate at decision threshold thr.
    FNR = FN / (FN + TP). Returns a fraction in [0,1].
    """
    y_true = y_true.astype(int)
    y_pred = (y_score >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    denom = (fn + tp)
    if denom == 0:
        return float("nan")
    return float(fn / denom)


def _brier(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Brier score (lower is better)."""
    y_true = y_true.astype(int)
    try:
        return float(brier_score_loss(y_true, np.clip(y_score, 0, 1)))
    except Exception:
        return float("nan")


def _round_none(x, ndigits: int = 3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return float("nan")
    return round(float(x), ndigits)


# ---------- main public function ----------

def compute_report_metrics(
    df: pd.DataFrame,
    score_col: str = "score",
    label_col: str = "label",
    sex_col: str = "sex",
    thr: float = 0.5,
) -> dict:
    """
    Compute the fields your EquityReport_template.md expects for a single dataset.

    Returns a dict containing:
      n_records, n_male, n_female, n_other, pct_female, representation_status,
      auroc_m, auroc_f, gap_auroc,
      fnr_m, fnr_f, gap_fnr,
      calib_gap,
      baseline_status
    """
    out: dict[str, object] = {}

    # --- clean / normalize ---
    df = df.copy()

    # normalize sex to 'M','F','O'
    df[sex_col] = (
        df[sex_col]
        .astype(str)
        .str.upper()
        .str.strip()
        .str[0]
        .map({"M": "M", "F": "F"})
        .fillna("O")
    )

    # ensure numeric
    df[label_col] = pd.to_numeric(df[label_col], errors="coerce")
    df[score_col] = pd.to_numeric(df[score_col], errors="coerce")
    df = df.dropna(subset=[label_col, score_col])

    # clip score to [0,1]
    df[score_col] = df[score_col].clip(0.0, 1.0)

    # --- representation counts ---
    n_records = int(len(df))
    n_female = int((df[sex_col] == "F").sum())
    n_male = int((df[sex_col] == "M").sum())
    n_other = int(n_records - n_female - n_male)
    pct_female = round((n_female / n_records * 100.0), 1) if n_records else 0.0

    # representation gate (≥45% female recommended)
    representation_status = "✅" if pct_female >= 45.0 else "⚠"

    out.update(
        {
            "n_records": n_records,
            "n_male": n_male,
            "n_female": n_female,
            "n_other": n_other,
            "pct_female": pct_female,
            "representation_status": representation_status,
        }
    )

    if n_records == 0:
        # nothing else to compute
        out.update(
            {
                "auroc_m": float("nan"),
                "auroc_f": float("nan"),
                "gap_auroc": float("nan"),
                "fnr_m": float("nan"),
                "fnr_f": float("nan"),
                "gap_fnr": float("nan"),
                "calib_gap": float("nan"),
                "baseline_status": "⚠",
            }
        )
        return out

    # --- split by sex ---
    df_m = df[df[sex_col] == "M"]
    df_f = df[df[sex_col] == "F"]

    y_m, s_m = df_m[label_col].values.astype(int), df_m[score_col].values.astype(float)
    y_f, s_f = df_f[label_col].values.astype(int), df_f[score_col].values.astype(float)

    # --- metrics by sex ---
    auroc_m = _safe_auroc(y_m, s_m)
    auroc_f = _safe_auroc(y_f, s_f)

    fnr_m = _fnr_at_threshold(y_m, s_m, thr)
    fnr_f = _fnr_at_threshold(y_f, s_f, thr)

    # Brier by sex; calibration gap is absolute difference
    brier_m = _brier(y_m, s_m) if len(df_m) else float("nan")
    brier_f = _brier(y_f, s_f) if len(df_f) else float("nan")
    calib_gap = (
        abs(brier_m - brier_f)
        if np.isfinite(brier_m) and np.isfinite(brier_f)
        else float("nan")
    )

    # --- gaps (as "percentage points" for AUROC/FNR like your template) ---
    # AUROC is [0,1]; display gap in percentage points
    gap_auroc = (
        abs(auroc_m - auroc_f) * 100.0
        if np.isfinite(auroc_m) and np.isfinite(auroc_f)
        else float("nan")
    )
    # FNR is fraction [0,1]; display gap in pp
    gap_fnr = (
        abs(fnr_m - fnr_f) * 100.0
        if np.isfinite(fnr_m) and np.isfinite(fnr_f)
        else float("nan")
    )

    # --- rounding to match report vibe ---
    auroc_m_r = _round_none(auroc_m, 3)
    auroc_f_r = _round_none(auroc_f, 3)
    gap_auroc_r = _round_none(gap_auroc, 2)

    fnr_m_r = _round_none(fnr_m * 100.0, 1) if np.isfinite(fnr_m) else float("nan")  # percent
    fnr_f_r = _round_none(fnr_f * 100.0, 1) if np.isfinite(fnr_f) else float("nan")  # percent
    gap_fnr_r = _round_none(gap_fnr, 1)

    calib_gap_r = _round_none(calib_gap, 3)

    out.update(
        {
            "auroc_m": auroc_m_r,
            "auroc_f": auroc_f_r,
            "gap_auroc": gap_auroc_r,          # in percentage points
            "fnr_m": fnr_m_r,                   # percent
            "fnr_f": fnr_f_r,                   # percent
            "gap_fnr": gap_fnr_r,               # in percentage points
            "calib_gap": calib_gap_r,           # absolute Brier delta
        }
    )

    # --- baseline status gate (same thresholds used in your report text) ---
    gates = []
    if np.isfinite(gap_auroc_r):
        gates.append(gap_auroc_r <= 2.0)         # ≤ 2 pp
    if np.isfinite(gap_fnr_r):
        gates.append(gap_fnr_r <= 5.0)           # ≤ 5 pp
    if np.isfinite(calib_gap_r):
        gates.append(calib_gap_r <= 0.05)        # ≤ 0.05
    # require representation gate too
    gates.append(representation_status == "✅")

    baseline_status = "✅" if all(gates) and len(gates) > 0 else "⚠"
    out["baseline_status"] = baseline_status

    return out
