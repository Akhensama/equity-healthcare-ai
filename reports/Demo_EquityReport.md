# **Equity Report – ER Triage (Admit vs Discharge)**

**Hospital:** Demo General Hospital

**Dataset size:** 20 patients (10 M / 10 F / 0 Other)

**Date generated:** 2025-09-12

**Version:** v0.1

---

## 1. Representation

- % Female patients: **50.0%**
- ⚠ Threshold check: ≥ 45% recommended
- Coverage by subgroup:
    - Chest pain (M: N/A, F: N/A)
    - Age <50 / ≥50 split by sex

✅ / ⚠ Indicator: ✅

---

## 2. Baseline Performance (Original Data)

| Metric | Male | Female | Gap | Threshold |
| --- | --- | --- | --- | --- |
| AUROC | 1.0 | 1.0 | 0.0 | ±2 pp |
| FNR @ 0.5 thr | 0.0% | 0.0% | 0.0 pp | ≤5 pp |
| Calibration Δ | – | – | 0.039 | ≤0.05 |

✅ / ⚠ Indicator: 

---

## 3. After Mitigation (Synthetic Balance)

**Method applied:** N/A (e.g., CTGAN female oversampling)

| Metric | Male | Female | Gap | Threshold |
| --- | --- | --- | --- | --- |
| AUROC | N/A | N/A | N/A | ±2 pp |
| FNR @ 0.5 thr | N/A% | N/A% | N/A pp | ≤5 pp |
| Calibration Δ | – | – | N/A | ≤0.05 |

✅ / ⚠ Indicator: ⚠

---

## 4. Privacy & Utility Checks (Synthetic Data)

- **Nearest neighbor distance:** N/A ≥ τ (⚠ ✅/⚠)
- **Membership inference AUC:** N/A ≈ 0.5 (⚠ ✅/⚠)
- **Utility drop (AUROC real vs syn):** N/A pp (≤2 pp ✅/⚠)

✅ / ⚠ Indicator: ⚠

---

## 5. Explainability Snapshot

- Top predictive features (all patients): N/A
- Sex-specific differences:
    - Male: N/A
    - Female: N/A

*(Visuals: SHAP plots auto-attached)*

---

## 6. Verdict

- **Overall Utility:** ⚠
- **Fairness:** ✅
- **Privacy:** ⚠

👉 **Recommendation:** Baseline computed. Mitigation not yet applied.

(e.g., “Synthetic balancing reduced FNR gap from 12 pp → 3 pp with negligible AUROC loss. Deploy in sandbox for further review.”)

---

## 7. Governance Notes

- Data de-identified before upload: Yes
- Misuse Policy acknowledged: Yes
- Review cycle: 6 months (next due 2026-03-12)

---

## ✅ / ⚠ Legend

- ✅ Passes threshold
- ⚠ Fails threshold → requires remediation

---

### 1. **Representation threshold (≥45% female)**

- **Why it matters:** if a dataset has too few women, the model mostly “learns” men’s patterns.
- **Why 45%:** real-world ER visits are close to 50/50 by sex. Allow some wiggle room, but <45% is a red flag.
- **Analogy:** if your class has 20 kids but only 6 are girls, the teacher may miss the girls’ needs.

---

### 2. **AUROC gap (≤2 percentage points)**

- **What AUROC is:** a score (0–1) of how good the model is at ranking “who should be admitted.”
- **Why ≤2pp:** if the model works much better for men than women, it’s unfair. 2pp is a common fairness tolerance in research.
- **Analogy:** two players both shoot ~70%. 70% vs. 72% is fine. 70% vs. 80% feels unfair.

---

### 3. **False Negative Rate gap (≤5 percentage points)**

- **What this means:** false negative = sending someone home when they should’ve been admitted.
- **Why ≤5pp:** clinical stakes are huge. We don’t want women going home 10–15% more often. ≤5pp is a practical fairness bar.
- **Analogy:** if referees call fouls 15% more on one team, the game feels rigged. A 3–5% wiggle is tolerable.

---

### 4. **Calibration gap (≤0.05 Brier delta)**

- **What calibration is:** if the model says “20% risk,” then ~20 of 100 patients like you should actually be admitted.
- **Why 0.05:** a bigger difference means systematic over/underestimation for one sex.
- **Analogy:** if your thermometer says 20°C but it’s really 25°C for girls and 20°C for boys, it’s biased.

---

### 5. **Privacy thresholds**

- **Nearest-neighbor distance ≥ τ:** ensures synthetic patients aren’t just clones of real patients.  
- **Membership inference AUC ≈ 0.5:** means attackers can’t guess if someone’s data was used. ~0.5 = safe.  
- **Utility drop ≤2pp:** synthetic data must still be useful. Too much drop = hospitals won’t trust it.