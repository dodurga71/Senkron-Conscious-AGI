from typing import Dict, Any, List
from .astro_predictor import AstroPredictor
from .financial_predictor import FinancialPredictor
from .chaos_predictor import ChaosPredictor
from .quantum_predictor import QuantumPredictor
from .geopolitical_predictor import GeopoliticalPredictor

class EnsemblePredictor:
    def __init__(self):
        self.mods = [
            AstroPredictor(), FinancialPredictor(),
            ChaosPredictor(), QuantumPredictor(), GeopoliticalPredictor()
        ]

    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        sigs: List[float] = []
        weights: List[float] = []
        unc: List[float] = []
        for m in self.mods:
            r = m.predict(features)
            sigs.append(r["signal"])
            weights.append(r["reliability"])
            unc.append(r["uncertainty"])
        total_w = sum(weights) or 1.0
        signal = sum(w*s for w, s in zip(weights, sigs)) / total_w
        uncertainty = sum(unc)/len(unc)
        reliability = min(1.0, sum(weights)/len(weights))
        return {"signal": signal, "uncertainty": uncertainty, "reliability": reliability}
