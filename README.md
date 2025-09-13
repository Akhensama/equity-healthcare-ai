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


