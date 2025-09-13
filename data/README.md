Equity in Healthcare AI

MOTIVE: Close gender gaps in healthcare data using synthetic data.

🚨 Problem Statement

Women in healthcare settings often face worse outcomes because clinical algorithms and datasets are biased toward male patients.

Post-operative mortality risk increases when women are treated by male surgeons.

Women with chest pain are more likely to be discharged than men, even when they need care.

This inequity leads to misdiagnosis, mistreatment, and avoidable harm.

🌍 Vision

A data platform that ensures healthcare AI works equally well for women by providing:

Synthetic female patient data

Fairness audits

Bias-mitigation tools

→ So hospitals can deliver safe, equitable care.

🚫 Non-Goals (for now)

Not replacing electronic health record (EHR) systems.

Not building new diagnostic algorithms from scratch.

Not tackling every equity axis at once (e.g., race, age, socioeconomic status).
Focus first: sex/gender.

🎯 MVP Slice

Emergency Room triage → predicting admission vs. discharge.

Why start here?

Public datasets exist (MIMIC-IV ICU/ED).

Clear binary outcome.

Documented disparities in triage scores by sex.

High impact for hospital partners.

🛠️ MVP Workflow: ER Triage (Admit vs. Discharge)

Input (Hospital uploads data)

Past ER records: vitals, labs, age, sex, outcome (admit/discharge).

Example: CSV/Excel with 100,000 patients.

Audit (System checks fairness)

% male vs. female patients.

Error rates (false negatives higher for women?).

Output: ⚠ warnings if disparities are found.

Synthetic Data Generation (Balance dataset)

Use CTGAN/SDV to create synthetic female patient records.

Synthetic data looks real but matches no actual person.

Privacy tests ensure no patient can be re-identified.

Model Training + Bias Mitigation (Sandbox)

Train predictive model (admit vs. discharge).

Compare:

Original (biased) vs. Balanced (fairer).

Output (Equity Report)

Representation of women in ER data.

Bias metrics (error rates, calibration gap).

Before/after mitigation.

Recommended strategies.

🏥 Impact

Hospital leadership → concrete evidence of bias.

Doctors → confidence that triage tools aren’t ignoring women.

Patients (esp. women) → fairer, safer admission decisions.

📊 Fairness Metrics (initial list)

Error-rate parity → false negatives/false positives by sex.

Calibration gap → predicted vs. actual risk across sexes.

Subgroup coverage → representation of female patients.

📂 Repo Structure
equity-healthcare-ai/
│
├── README.md                # project overview (this file)
├── governance/              # governance & ethics docs
│   ├── DPIA_template.md
│   ├── fairness_metrics.md
│
├── data/
│   ├── raw/                 # real datasets (later)
│   ├── synthetic/           # SDV-generated CSVs
│   ├── fake_er.csv          # toy dataset for demo
│   └── README.md
│
├── synthetic/
│   ├── ctgan_baseline.ipynb
│   ├── tvae_experiment.ipynb
│
├── model/
│   ├── baseline_classifier.ipynb
│   ├── bias_audit.ipynb
│
├── app/
│   ├── reporting/
│   │   ├── compute_metrics.py
│   │   ├── generate_equity_report.py
│   │   ├── metrics_example.py
│   │   └── run_demo.py
│   ├── streamlit_app.py
│   └── requirements.txt
│
└── reports/
    ├── EquityReport_template.md   # template with {{placeholders}}
    ├── DataCard_template.md
    └── Demo_EquityReport.md       # generated demo report

📜 DPIA (Data Protection Impact Assessment) Outline

Purpose: Generate synthetic patient data + audit algorithms for fairness across sex.

Data Types: Demographics, vitals, labs, admission outcome.

Risks: Re-identification, misuse of synthetic data, algorithmic harm.

Safeguards:

De-identification of real data.

Privacy tests for synthetic data.

Advisory board review.

Impact: Improved equity in clinical decision support.

Next Review: Every 6 months.