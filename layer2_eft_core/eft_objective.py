from __future__ import annotations

import numpy as np


def s_ee(C: np.ndarray) -> float:
    """Yer tutucu 'entanglement entropy' benzeri ölçü: log(det(I + C))."""
    n = C.shape[0]
    eye = np.eye(n)
    val = float(np.log(np.linalg.det(eye + C + 1e-6 * eye)))
    return max(val, 0.0)


def expected_kr(signals: dict[str, dict]) -> float:
    vals = [abs(v.get("signal", 0.0)) * (1.0 - v.get("uncertainty", 0.5)) for v in signals.values()]
    return float(np.mean(vals)) if vals else 0.0


def f_info(signals: dict[str, dict], C: np.ndarray, alpha: float = 0.1) -> float:
    return expected_kr(signals) - alpha * s_ee(C)
