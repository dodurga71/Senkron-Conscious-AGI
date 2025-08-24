"""
Katman 4 - Metrik & Enerji Ölçüm Planı (İskelet)
- compute_accuracy: basit örnek
- measure_energy_usage: süre tabanlı minimal ölçüm
Not: İlerde psutil/raporlama eklenecek.
"""

import time
from typing import Sequence


def compute_accuracy(pred: Sequence, true: Sequence) -> float:
    if not pred and not true:
        return 1.0
    if not pred or not true or len(pred) != len(true):
        return 0.0
    correct = sum(1 for p, t in zip(pred, true, strict=False) if p == t)
    return correct / len(true)


def measure_energy_usage():
    start = time.perf_counter()
    # Placeholder "iş"
    _ = sum(range(10_000))
    elapsed = time.perf_counter() - start
    return {"energy_proxy_seconds": elapsed}
