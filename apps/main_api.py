from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from config.settings import get_settings
from layer1_prediction_engine.ensemble import EnsemblePredictor
from layer2_eft_core.ce_state import CEState
from layer2_eft_core.eft_objective import f_info
from layer3_communication.storyteller import build_narrative
from onur_module.router import router as onur_router

app = FastAPI(title="SENKRON API", version="0.2.0")


class FeaturesIn(BaseModel):
    features: dict[str, Any] = Field(default_factory=dict)


class InterpretationOut(BaseModel):
    nlg: dict[str, Any]
    raw: dict[str, Any]
    meta: dict[str, Any]


def _bump_metrics():
    """Yalın sayaç: her tahminde günün metrics JSONL dosyasına bir satır ekle."""
    s = get_settings()
    metrics_dir = Path(s.METRICS_DIR)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    dayfile = metrics_dir / (datetime.now(UTC).strftime("%Y-%m-%d") + ".jsonl")
    rec = {
        "ts": datetime.now(UTC).isoformat(),
        "event": "predict",  # içerik önemli değil; CalibMonitor satır sayıyor
    }
    with dayfile.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


@app.get("/healthz")
def healthz():
    s = get_settings()
    return {"ok": True, "service": "senkron", "version": s.APP_VERSION}


@app.post("/forecast/interpret", response_model=InterpretationOut)
def interpret_forecast(inp: FeaturesIn):
    # 1) Ensemble tahmin
    ens = EnsemblePredictor()
    fused = ens.predict(inp.features)
    source_names = [m.name for m in getattr(ens, "mods", [])]  # raw.sources için

    # 2) EFT: CE ve F_info
    signals = {"ensemble": {"signal": fused["signal"], "uncertainty": fused["uncertainty"]}}
    ce = CEState.from_signals(signals)
    score = f_info(signals, ce.C, alpha=0.1)

    # 3) Anlatı
    nlg = build_narrative(
        signal=fused["signal"],
        uncertainty=fused["uncertainty"],
        reliability=fused["reliability"],
        sources=["astro", "finance", "chaos", "quantum", "geopolitical"],
    )

    # 4) Sayaç dosyasına bir satır yaz (n artışı)
    _bump_metrics()

    return {
        "nlg": nlg,
        "raw": {
            "signal": fused["signal"],
            "uncertainty": fused["uncertainty"],
            "reliability": fused["reliability"],
            "f_info": round(score, 6),
            "ce_dim": ce.meta["dim"],
            "sources": source_names,  # <<— test_nlg_sources bekliyor
        },
        "meta": {"schema": "v1", "engine": "senkron"},
    }


# Onur modülü (read-only)
app.include_router(onur_router)
