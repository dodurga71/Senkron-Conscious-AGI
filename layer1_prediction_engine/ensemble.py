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

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        sigs: List[float] = []
        weights: List[float] = []
        unc: List[float] = []
        details: List[Dict[str, float]] = []

        for m in self.mods:
            r = m.predict(features)
            sigs.append(r["signal"])
            weights.append(r["reliability"])
            unc.append(r["uncertainty"])
            details.append({
                "name": m.name,
                "signal": r["signal"],
                "uncertainty": r["uncertainty"],
                "reliability": r["reliability"],
            })

        total_w = sum(weights) or 1.0
        signal = sum(w*s for w, s in zip(weights, sigs)) / total_w
        uncertainty = sum(unc) / len(unc)
        reliability = min(1.0, sum(weights) / len(weights))

        # katkı (ağırlıklı sinyal payı)
        contribs = [(w*s)/total_w for w, s in zip(weights, sigs)]
        for d, c in zip(details, contribs):
            d["contribution"] = c

        # sürücüler (mutlak katkıya göre sıralı)
        details.sort(key=lambda x: abs(x.get("contribution", 0.0)), reverse=True)

        return {
            "signal": signal,
            "uncertainty": uncertainty,
            "reliability": reliability,
            "sources": details  # nlg için zengin içerik
        }
