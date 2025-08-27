from __future__ import annotations

import math
from collections.abc import Iterable


def brier_score(y_true: Iterable[int], p_hat: Iterable[float]) -> float:
    y = list(y_true)
    p = list(p_hat)
    if len(y) != len(p) or len(y) == 0:
        raise ValueError("y and p lengths must match and be > 0")
    return sum((yi - pi) ** 2 for yi, pi in zip(y, p, strict=False)) / len(y)


def log_loss(y_true: Iterable[int], p_hat: Iterable[float], eps: float = 1e-12) -> float:
    y = list(y_true)
    p = [min(max(pi, eps), 1 - eps) for pi in p_hat]
    if len(y) != len(p) or len(y) == 0:
        raise ValueError("y and p lengths must match and be > 0")
    return -sum(yi * math.log(pi) + (1 - yi) * math.log(1 - pi) for yi, pi in zip(y, p, strict=False)) / len(y)


class OnlineCalibration:
    """Basit çevrim-içi metrik toplayıcı (binary)."""

    def __init__(self) -> None:
        self.n = 0
        self._brier_sum = 0.0
        self._logloss_sum = 0.0

    def update_binary(self, y_true: int, p_hat: float, eps: float = 1e-12) -> None:
        p = min(max(float(p_hat), eps), 1 - eps)
        self.n += 1
        self._brier_sum += (y_true - p) ** 2
        self._logloss_sum += -(y_true * math.log(p) + (1 - y_true) * math.log(1 - p))

    @property
    def metrics(self):
        if self.n == 0:
            return {"brier": None, "logloss": None, "n": 0}
        return {
            "brier": self._brier_sum / self.n,
            "logloss": self._logloss_sum / self.n,
            "n": self.n,
        }
