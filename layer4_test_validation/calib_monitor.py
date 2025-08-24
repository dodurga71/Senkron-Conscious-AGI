from __future__ import annotations
from typing import Dict, Any
from pathlib import Path
from datetime import datetime, timezone
import json

from layer1_prediction_engine.calibration import OnlineCalibration
from tracking.mlflow_logger import log_metric

class CalibMonitor:
    def __init__(self) -> None:
        self.oc = OnlineCalibration()

    def update(self, y_true: int, p_hat: float) -> None:
        self.oc.update_binary(int(y_true), float(p_hat))

    def snapshot(self) -> Dict[str, Any]:
        return self.oc.metrics

    def flush_daily(self, out_dir: str = "logs/metrics") -> str:
        m = self.snapshot()
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        path = Path(out_dir) / (datetime.now(timezone.utc).strftime("%Y-%m-%d") + ".jsonl")
        rec = {"ts": datetime.now(timezone.utc).isoformat(), **m}
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if m.get("brier") is not None:
            log_metric("brier", float(m["brier"]))
            log_metric("logloss", float(m["logloss"]))
        return str(path)

calib_monitor = CalibMonitor()
