from __future__ import annotations

from typing import Dict


def eap_clamp(hyperparams: Dict[str, float]) -> Dict[str, float]:
    """EAP: hiperparametreleri güvenli aralıklara kelepçeler."""
    hp = dict(hyperparams)
    hp["lr"] = min(max(hp.get("lr", 1e-3), 1e-5), 1e-1)
    hp["temp"] = min(max(hp.get("temp", 1.0), 0.1), 5.0)
    return hp
