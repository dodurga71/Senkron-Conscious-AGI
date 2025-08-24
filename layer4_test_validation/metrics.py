"""
Katman 4 - Metrik & Enerji Ölçüm Planı
- compute_accuracy: basit örnek
- measure_energy_usage:
    * Her zaman "energy_proxy_seconds" + "wall_seconds" döndürür (stabil şema).
    * psutil varsa ek olarak cpu_user_delta, cpu_system_delta, rss_mb anahtarlarını ekler.
"""

import os
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
    start_wall = time.perf_counter()
    try:
        import psutil  # type: ignore

        p = psutil.Process(os.getpid())
        cpu0 = p.cpu_times()

        # Placeholder hesap yükü
        _ = sum(range(50_000))

        wall = time.perf_counter() - start_wall
        cpu1 = p.cpu_times()
        rss_mb = p.memory_info().rss / 1e6

        return {
            "wall_seconds": wall,
            "energy_proxy_seconds": wall,  # geri uyumlu alan
            "cpu_user_delta": getattr(cpu1, "user", 0.0) - getattr(cpu0, "user", 0.0),
            "cpu_system_delta": getattr(cpu1, "system", 0.0)
            - getattr(cpu0, "system", 0.0),
            "rss_mb": rss_mb,
        }
    except Exception:
        # psutil yoksa sadece süre temelli geri uyumlu alanlar
        _ = sum(range(50_000))
        wall = time.perf_counter() - start_wall
        return {
            "wall_seconds": wall,
            "energy_proxy_seconds": wall,
        }
