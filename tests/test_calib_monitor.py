import json
from pathlib import Path

from layer4_test_validation.calib_monitor import CalibMonitor


def test_calib_monitor_flush(tmp_path):
    m = CalibMonitor()
    m.update(1, 0.8)
    m.update(0, 0.2)
    out = m.flush_daily(out_dir=str(tmp_path))
    p = Path(out)
    assert p.exists()
    lines = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines()]
    assert len(lines) >= 1 and "brier" in lines[-1] and "logloss" in lines[-1]
