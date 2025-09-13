from jinja2 import Template
from pathlib import Path
import sys
import traceback

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "reports" / "EquityReport_template.md"

def generate_equity_report(metrics: dict, output_path):
    print(f"[INFO] Template path: {TEMPLATE_PATH}")
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found at: {TEMPLATE_PATH}")

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    print(f"[INFO] Template size: {len(template_text)} chars")

    report = Template(template_text).render(**metrics)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"[OK] Wrote report to: {output_path.resolve()}")
    return str(output_path)

if __name__ == "__main__":
    try:
        from .metrics_example import example_metrics
        generate_equity_report(example_metrics, TEMPLATE_PATH.parent / "Demo_EquityReport.md")
    except Exception as e:
        print("[ERROR] Report generation failed:")
        traceback.print_exc()
        sys.exit(1)
