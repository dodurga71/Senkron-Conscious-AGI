import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config.settings import get_settings
from tracking.mlflow_logger import log_metric  # no-op

Number = int | float


class CalibMonitor:
    def __init__(self) -> None:
        self._brier_sum: float = 0.0
        self._logloss_sum: float = 0.0
        self._n: int = 0

    def _metrics_dir(self) -> Path:
        return Path(get_settings().METRICS_DIR)

    @staticmethod
    def _clip(p: Number, eps: float = 1e-12) -> float:
        p = float(p)
        if p < eps:
            return eps
        if p > 1.0 - eps:
            return 1.0 - eps
        return p

    def update(self, y_true: Number, y_prob: Number) -> int:
        y = 1.0 if float(y_true) >= 0.5 else 0.0
        p = self._clip(y_prob)
        self._brier_sum += (p - y) ** 2
        self._logloss_sum += -(y * math.log(p) + (1.0 - y) * math.log(1.0 - p))
        self._n += 1
        return self._n

    def _averages(self):
        if self._n == 0:
            return None, None
        return self._brier_sum / self._n, self._logloss_sum / self._n

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

    def flush(self, out_dir: str | Path | None = None) -> str:
        """Günün dosyasına bir satır yazar ve dosya yolunu döndürür."""
        brier, logloss = self._averages()
        rec = {"brier": brier, "logloss": logloss, "n": self._n}

        d = Path(out_dir) if out_dir is not None else self._metrics_dir()
        d.mkdir(parents=True, exist_ok=True)
        fname = datetime.now(UTC).strftime("%Y-%m-%d") + ".jsonl"
        out_path = d / fname

        with out_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        try:
            if brier is not None:
                log_metric("avg_brier", float(brier))
            if logloss is not None:
                log_metric("avg_logloss", float(logloss))
        except Exception:
            pass

        return str(out_path)

    # TEST'in beklediği isim:
    def flush_daily(self, out_dir: str | Path | None = None) -> str:
        return self.flush(out_dir=out_dir)

    def snapshot(self) -> dict[str, Any]:
        brier, logloss = self._averages()
        n_disk = self.count_predictions()
        n = max(self._n, n_disk)
        return {"brier": brier, "logloss": logloss, "n": n}


calib_monitor = CalibMonitor()
