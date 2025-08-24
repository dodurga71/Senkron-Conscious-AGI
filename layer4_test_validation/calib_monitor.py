from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import get_settings
from tracking.mlflow_logger import log_metric  # no-op; kalsın

class CalibMonitor:
    """Basit kalibrasyon izleyici. n = METRICS_DIR altındaki jsonl satır sayısı."""
    def __init__(self) -> None:
        self._brier: Optional[float] = None
        self._logloss: Optional[float] = None

    def _metrics_dir(self) -> Path:
        return Path(get_settings().METRICS_DIR)

    def count_predictions(self) -> int:
        d = self._metrics_dir()
        if not d.exists():
            return 0
        n = 0
        for p in d.glob("*.jsonl"):
            try:
                with p.open("r", encoding="utf-8") as f:
                    for _ in f:
                        n += 1
            except FileNotFoundError:
                pass
        return n

    def snapshot(self) -> Dict[str, Any]:
        return {
            "brier": self._brier,
            "logloss": self._logloss,
            "n": self.count_predictions(),
        }

calib_monitor = CalibMonitor()
