equity-healthcare-ai

Prototype for fairness and equity reporting in healthcare ML models using synthetic balancing.
This project helps evaluate gender representation and bias in clinical prediction tasks (e.g., ER triage) and tests mitigation approaches like CTGAN oversampling.

⚠️ Disclaimer: This is a research prototype, not for clinical use.

✨ Features

📊 Before/After comparison of fairness metrics (AUROC, FNR, Calibration).

👩‍⚕️ Representation check (e.g., % female patients).

🧪 Synthetic data mitigation using generative models (e.g., CTGAN).

📝 Generates a Markdown equity report ready for sharing.

🔒 Includes privacy & utility placeholders for future testing.

📂 Project Structure

equity-healthcare-ai/
│
├── app/
│   └── reporting/              # Core reporting logic
│       ├── compute_metrics.py
│       ├── generate_equity_report.py
│       └── run_demo.py          # Entry point
│
├── data/                        # Example CSVs
│   ├── imbalanced.csv
│   └── synthetic/
│       └── balanced_ctgan.csv
│
├── reports/                     # Output reports
│   └── BeforeAfter_EquityReport.md
│
├── governance/                  # Templates for compliance
│   ├── DPIA_template.md
│   └── fairness_metrics.md
│
├── requirements.txt             # Dependencies
└── README.md


Installation

Clone the repo and install dependencies:

git clone https://github.com/defnecolak/equity-healthcare-ai.git
cd equity-healthcare-ai

Re-install deps inside the activated venv:

python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt

Run your pipeline:
python app\synthetic\balance_with_ctgan.py --csv data\imbalanced.csv --out data\synthetic\balanced.csv --epochs 300


# Build the report
python -m app.reporting.run_demo `
  --csv_before data\imbalanced.csv `
  --csv_after  data\synthetic\balanced.csv `
  --out reports\BeforeAfter_EquityReport.md `
  --thr 0.5


# Open the report
notepad reports\BeforeAfter_EquityReport.md

Example Output (Based on my test):

# Equity Report - ER Triage (Admit vs Discharge)

Hospital: Demo General Hospital  
Dataset size: 20 patients (14 M / 6 F / 0 Other)  
Date generated: 2025-09-13  
Version: v0.1

---

## 1) Representation

- % Female patients: 30.0%
- Threshold check: >= 45% recommended
- Coverage by subgroup:
  - Chest pain (M: , F: )
  - Age <50 / >=50 split by sex

Status: FAIL (PASS or FAIL)

---

## 2) Baseline Performance (Original Data)

| Metric              | Male        | Female      | Gap (F-M, pp) | Threshold |
|---------------------|-------------|-------------|---------------|-----------|
| AUROC               | 1.0 | 1.0 | 0.0 | <= 2 pp   |
| FNR @ thr=0.5       | 0.0%  | 0.0%  | 0.0   | <= 5 pp   |
| Calibration Delta   | -           | -           | 0.06 | <= 0.05   |

Status: FAIL (PASS or FAIL)

---

## 3) After Mitigation (Synthetic Balance)

Method applied: CTGAN female oversampling (example: CTGAN female oversampling)

| Metric              | Male            | Female          | Gap (F-M, pp)     | Threshold |
|---------------------|-----------------|-----------------|-------------------|-----------|
| AUROC               | 1.0 | 0.833 | 16.67 | <= 2 pp   |
| FNR @ thr=0.5       | 0.0%  | 16.7%  | 16.7   | <= 5 pp   |
| Calibration Delta   | -               | -               | 0.173 | <= 0.05   |

Status: FAIL (PASS or FAIL)

Change vs baseline:
- Female ratio: 30.0% -> 41.7%
- AUROC gap: 0.0 -> 16.67
- FNR gap: 0.0 pp -> 16.7 pp
- Calibration Delta: 0.06 -> 0.173

---

## 4) Privacy & Utility (Synthetic Data)

- Nearest neighbor distance: N/A >= tau -> FAIL
- Membership inference AUC: N/A ~0.5 -> FAIL
- Utility drop (AUROC real vs syn): N/A pp (<= 2 pp recommended)

Status: FAIL (PASS or FAIL)

---

## 5) Verdict & Recommendation

Overall Utility: FAIL  
Fairness: FAIL  
Privacy: FAIL  

Recommendation: FNR gap 0.0 pp -> 16.7 pp (up by 16.7 pp) ; AUROC gap 0.0 pp -> 16.67 pp. Recommend sandbox evaluation with clinical review.

---

Notes:
- "pp" = percentage points  
- PASS means threshold met, FAIL means threshold not met  
- Report is a prototype, not for clinical use



Contributing:

This is an early-stage prototype. Contributions are welcome!

Improve fairness metrics

Add new mitigation strategies (SMOTE, TVAE, etc.)

Expand privacy checks

Fork the repo, make your changes, and open a pull request.

How to Use:

This project generates fairness and equity reports for healthcare ML models using synthetic balancing (CTGAN, SMOTE, TVAE, etc.).

1. Clone the repo
git clone https://github.com/defnecolak/equity-healthcare-ai.git
cd equity-healthcare-ai

2. Set up environment

Make sure you have Python 3.11+ installed. Then create a virtual environment:

python -m venv .venv
.venv\Scripts\activate    # (Windows PowerShell)
# or
source .venv/bin/activate # (Linux / MacOS)

Install dependencies:
pip install -r requirements.txt

3. Run synthetic balancing (optional)

Generate a balanced dataset with CTGAN:

python app/synthetic/balance_with_ctgan.py \
  --csv data/imbalanced.csv \
  --out data/synthetic/balanced_ctgan.csv \
  --epochs 300

  This will create:
📂 data/synthetic/balanced_ctgan.csv

4. Generate equity report

Run the reporting module:
python -m app.reporting.run_demo \
  --csv_before data/imbalanced.csv \
  --csv_after data/synthetic/balanced_ctgan.csv \
  --out reports/EquityReport.md \
  --thr 0.5

5.View results

The report will be saved as:

📄 reports/EquityReport.md

You can open it:

In VS Code (supports Markdown preview)

On GitHub (renders automatically)

Or quick check in terminal:
type reports/EquityReport.md

Note: This tool is a prototype, not for clinical use. It’s designed to demonstrate fairness reporting workflows.



License:

MIT License — free to use, modify, and share.


