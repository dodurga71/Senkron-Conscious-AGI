from __future__ import annotations


def eap_clamp(hyperparams: dict[str, float]) -> dict[str, float]:
    """EAP: hiperparametreleri güvenli aralıklara kelepçeler."""
    hp = dict(hyperparams)
    hp["lr"] = min(max(hp.get("lr", 1e-3), 1e-5), 1e-1)
    hp["temp"] = min(max(hp.get("temp", 1.0), 0.1), 5.0)
    return hp
