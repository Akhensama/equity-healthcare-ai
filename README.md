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
pip install -r requirements.txt

Usage

Run the demo report with example data:

python -m app.reporting.run_demo \
  --csv_before data/imbalanced.csv \
  --csv_after data/synthetic/balanced_ctgan.csv \
  --out reports/BeforeAfter_EquityReport.md \
  --thr 0.5
This will generate a Markdown report in reports/BeforeAfter_EquityReport.md.

Example Output:

## 1. Representation
- % Female patients: 30.0%
- Threshold check: FAIL (≥ 45% recommended)

## 2. Baseline Performance (Original Data)
AUROC gap: 0.0 pp
FNR gap: 0.0 pp
Calibration delta: 0.06

## 3. After Mitigation (Synthetic Balance)
Method: CTGAN oversampling
AUROC gap: 12.0 pp
FNR gap: 20.0 pp
Calibration delta: 0.105

## 5. Verdict & Recommendation
Overall Utility: FAIL
Fairness: FAIL
Privacy: FAIL
Recommendation: Sandbox evaluation with clinical review.

Contributing:

This is an early-stage prototype. Contributions are welcome!

Improve fairness metrics

Add new mitigation strategies (SMOTE, TVAE, etc.)

Expand privacy checks

Fork the repo, make your changes, and open a pull request.

License:

MIT License — free to use, modify, and share.


