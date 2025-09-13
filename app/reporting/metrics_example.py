example_metrics = {
    "hospital_name": "Demo General Hospital",
    "n_records": 100000,
    "n_male": 65000,
    "n_female": 35000,
    "n_other": 0,
    "date": "2025-09-12",

    "pct_female": 35,
    "representation_status": "⚠",

    "n_male_chest": 12000,
    "n_female_chest": 6000,

    "auroc_m": 0.79,
    "auroc_f": 0.73,
    "gap_auroc": -0.06,
    "fnr_m": 12,
    "fnr_f": 20,
    "gap_fnr": 8,
    "calib_gap": 0.07,
    "baseline_status": "⚠",

    "method_name": "CTGAN female oversampling",
    "auroc_m_syn": 0.78,
    "auroc_f_syn": 0.77,
    "gap_auroc_syn": -0.01,
    "fnr_m_syn": 13,
    "fnr_f_syn": 14,
    "gap_fnr_syn": 1,
    "calib_gap_syn": 0.03,
    "mitigation_status": "✅",

    "nn_distance": 0.45,
    "privacy_pass": "✅",
    "mia_auc": 0.51,
    "mia_pass": "✅",
    "utility_drop": 1,
    "privacy_status": "✅",

    "features_global": "heart_rate, O2_sat, chest_pain_flag",
    "features_male": "troponin, age, diabetes",
    "features_female": "chest_pain_flag, heart_rate, O2_sat",

    "utility_flag": "✅",
    "fairness_flag": "✅",
    "privacy_flag": "✅",
    "recommendation_text": "Synthetic balancing reduced FNR gap from 8 pp → 1 pp with negligible AUROC loss.",
    "yes_no": "Yes",
    "next_review_date": "2026-03-12"
}
