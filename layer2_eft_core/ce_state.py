from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np


@dataclass
class CEState:
    """Dolanım kovaryans matrisi için basit durum kabı."""

    C: np.ndarray
    meta: Dict[str, Any]

    @classmethod
    def from_signals(cls, signals: Dict[str, Dict[str, float]]) -> "CEState":
        vec = np.array(
            [float(v.get("signal", 0.0)) for v in signals.values()], dtype=float
        )
        if vec.size == 0:
            vec = np.zeros(1)
        C = np.outer(vec, vec)  # yer tutucu
        return cls(C=C, meta={"dim": int(vec.size)})
