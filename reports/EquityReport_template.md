# Equity Report - ER Triage (Admit vs Discharge)

Hospital: {{hospital_name}}  
Dataset size: {{n_records}} patients ({{n_male}} M / {{n_female}} F / {{n_other}} Other)  
Date generated: {{date}}  
Version: {{version}}

---

## 1) Representation

- % Female patients: {{pct_female}}%
- Threshold check: >= 45% recommended
- Coverage by subgroup:
  - Chest pain (M: {{n_male_chest}}, F: {{n_female_chest}})
  - Age <50 / >=50 split by sex

Status: {{representation_status}} (PASS or FAIL)

---

## 2) Baseline Performance (Original Data)

| Metric              | Male        | Female      | Gap (F-M, pp) | Threshold |
|---------------------|-------------|-------------|---------------|-----------|
| AUROC               | {{auroc_m}} | {{auroc_f}} | {{gap_auroc}} | <= 2 pp   |
| FNR @ thr=0.5       | {{fnr_m}}%  | {{fnr_f}}%  | {{gap_fnr}}   | <= 5 pp   |
| Calibration Delta   | -           | -           | {{calib_gap}} | <= 0.05   |

Status: {{baseline_status}} (PASS or FAIL)

---

## 3) After Mitigation (Synthetic Balance)

Method applied: {{method_name}} (example: CTGAN female oversampling)

| Metric              | Male            | Female          | Gap (F-M, pp)     | Threshold |
|---------------------|-----------------|-----------------|-------------------|-----------|
| AUROC               | {{auroc_m_syn}} | {{auroc_f_syn}} | {{gap_auroc_syn}} | <= 2 pp   |
| FNR @ thr=0.5       | {{fnr_m_syn}}%  | {{fnr_f_syn}}%  | {{gap_fnr_syn}}   | <= 5 pp   |
| Calibration Delta   | -               | -               | {{calib_gap_syn}} | <= 0.05   |

Status: {{mitigation_status}} (PASS or FAIL)

Change vs baseline:
- Female ratio: {{pct_female}}% -> {{pct_female_syn}}%
- AUROC gap: {{gap_auroc}} -> {{gap_auroc_syn}}
- FNR gap: {{gap_fnr}} pp -> {{gap_fnr_syn}} pp
- Calibration Delta: {{calib_gap}} -> {{calib_gap_syn}}

---

## 4) Privacy & Utility (Synthetic Data)

- Nearest neighbor distance: {{nn_distance}} >= tau -> {{privacy_pass}}
- Membership inference AUC: {{mia_auc}} ~0.5 -> {{mia_pass}}
- Utility drop (AUROC real vs syn): {{utility_drop}} pp (<= 2 pp recommended)

Status: {{privacy_status}} (PASS or FAIL)

---

## 5) Verdict & Recommendation

Overall Utility: {{utility_flag}}  
Fairness: {{fairness_flag}}  
Privacy: {{privacy_flag}}  

Recommendation: {{recommendation_text}}

---

Notes:
- "pp" = percentage points  
- PASS means threshold met, FAIL means threshold not met  
- Report is a prototype, not for clinical use
