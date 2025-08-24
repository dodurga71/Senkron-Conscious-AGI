from typing import Any, Dict

from .base import BasePredictor


class AstroPredictor(BasePredictor):
    name = "astro_predictor"

    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        score = 0.1 if features.get("moon_phase") == "waxing" else -0.05
        return {
            "signal": self.clamp(score, -1, 1),
            "uncertainty": 0.4,
            "reliability": 0.6,
        }
