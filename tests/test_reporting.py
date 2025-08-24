import json
from pathlib import Path

from layer4_test_validation.reporting import generate_dashboard


def _write_jsonl(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def test_generate_dashboard(tmp_path):
    metrics_dir = tmp_path / "logs" / "metrics"
    # iki günlük sahte kayıtlar (son satır en güncel olacak şekilde)
    _write_jsonl(
        metrics_dir / "2025-08-23.jsonl",
        [
            {"brier": 0.12, "logloss": 0.45, "n": 5},
            {"brier": 0.11, "logloss": 0.40, "n": 8},
        ],
    )
    _write_jsonl(
        metrics_dir / "2025-08-24.jsonl",
        [
            {"brier": 0.10, "logloss": 0.39, "n": 10},
        ],
    )

    out_csv = tmp_path / "history.csv"
    out_md = tmp_path / "report.md"

    csv_p, md_p = generate_dashboard(
        metrics_dir=str(metrics_dir),
        out_csv=str(out_csv),
        out_md=str(out_md),
    )

    assert Path(csv_p).exists()
    assert Path(md_p).exists()
    md_text = Path(md_p).read_text(encoding="utf-8")
    assert "Kalibrasyon Raporu" in md_text
