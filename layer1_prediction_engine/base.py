from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePredictor(ABC):
    name: str = "base"

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        """
        Döndür: {"signal": float (-1..+1), "uncertainty": float (0..1), "reliability": float (0..1)}
        """
        ...

    def clamp(self, x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))
