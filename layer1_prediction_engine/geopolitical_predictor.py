from typing import Any, Dict

from .base import BasePredictor


class GeopoliticalPredictor(BasePredictor):
    name = "geopolitical_predictor"

    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        risk = float(features.get("risk_index", 0.0))
        score = -0.1 if risk > 0.5 else 0.05
        return {
            "signal": self.clamp(score, -1, 1),
            "uncertainty": 0.35,
            "reliability": 0.65,
        }
