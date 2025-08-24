from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any

from onur_module.router import router as onur_router
from layer1_prediction_engine.ensemble import EnsemblePredictor
from layer2_eft_core.ce_state import CEState
from layer2_eft_core.eft_objective import f_info
from layer3_communication.storyteller import build_narrative
from layer4_test_validation.calib_monitor import calib_monitor

app = FastAPI(title="SENKRON API", version="0.4.0")

class FeaturesIn(BaseModel):
    features: Dict[str, Any] = Field(default_factory=dict)

class InterpretationOut(BaseModel):
    nlg: Dict[str, Any]
    raw: Dict[str, Any]
    meta: Dict[str, Any]

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "senkron", "version": "0.4.0"}

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
        sources=["astro","finance","chaos","quantum","geopolitical"],
        source_details=fused.get("sources")
    )

    # DEMO kalibrasyon: proxy etiket + olasılık
    momentum = float(inp.features.get("momentum", 0.0))
    y_true = 1 if momentum >= 0 else 0
    p_hat = max(0.0, min(1.0, (fused["signal"] + 1.0) / 2.0))  # [-1,1] → [0,1]
    calib_monitor.update(y_true, p_hat)
    calib_path = calib_monitor.flush_daily()

    return {
        "nlg": nlg,
        "raw": {
            "signal": fused["signal"],
            "uncertainty": fused["uncertainty"],
            "reliability": fused["reliability"],
            "f_info": round(score, 6),
            "ce_dim": ce.meta["dim"],
            "sources": fused.get("sources", [])
        },
        "meta": {"schema": "v1", "engine": "senkron", "calibration_log": calib_path}
    }

app.include_router(onur_router)
