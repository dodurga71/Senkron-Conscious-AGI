from fastapi import APIRouter
from typing import Dict
from layer2_eft_core.ce_state import CEState
from layer2_eft_core.eft_objective import f_info

router = APIRouter(prefix="/onur", tags=["onur-module"])

_SAMPLE: Dict[str, Dict[str, float]] = {
    "astro": {"signal": 0.05, "uncertainty": 0.4},
    "finance": {"signal": 0.12, "uncertainty": 0.3},
    "social": {"signal": -0.01, "uncertainty": 0.5},
}

@router.get("/state/ce")
def get_ce_state():
    ce = CEState.from_signals(_SAMPLE)
    return {"dim": ce.meta["dim"], "C": ce.C.tolist()}

@router.get("/forecasts/raw")
def get_raw_forecasts():
    ce = CEState.from_signals(_SAMPLE)
    score = f_info(_SAMPLE, ce.C, alpha=0.1)
    return {"signals": _SAMPLE, "f_info": round(score, 6)}
