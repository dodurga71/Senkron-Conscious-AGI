from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any

from onur_module.router import router as onur_router
from layer1_prediction_engine.ensemble import EnsemblePredictor
from layer2_eft_core.ce_state import CEState
from layer2_eft_core.eft_objective import f_info
from layer3_communication.storyteller import build_narrative
from config.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

class FeaturesIn(BaseModel):
    features: Dict[str, Any] = Field(default_factory=dict)

class InterpretationOut(BaseModel):
    nlg: Dict[str, Any]
    raw: Dict[str, Any]
    meta: Dict[str, Any]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "senkron", "version": settings.APP_VERSION}

@app.post("/forecast/interpret", response_model=InterpretationOut)
def interpret_forecast(inp: FeaturesIn):
    ens = EnsemblePredictor()
    fused = ens.predict(inp.features)
    signals = {"ensemble": {"signal": fused["signal"], "uncertainty": fused["uncertainty"]}}
    ce = CEState.from_signals(signals)
    score = f_info(signals, ce.C, alpha=0.1)
    nlg = build_narrative(
        signal=fused["signal"],
        uncertainty=fused["uncertainty"],
        reliability=fused["reliability"],
        sources=["astro","finance","chaos","quantum","geopolitical"]
    )
    return {
        "nlg": nlg,
        "raw": {
            "signal": fused["signal"],
            "uncertainty": fused["uncertainty"],
            "reliability": fused["reliability"],
            "f_info": round(score, 6),
            "ce_dim": ce.meta["dim"]
        },
        "meta": {"schema": "v1", "engine": "senkron"}
    }

app.include_router(onur_router)
