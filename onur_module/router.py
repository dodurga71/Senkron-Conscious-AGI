from fastapi import APIRouter
from layer4_test_validation.calib_monitor import calib_monitor
from layer2_eft_core.ce_state import CEState

router = APIRouter(prefix="/onur", tags=["onur"])

@router.get("/ping")
def ping():
    return {"ok": True}

@router.get("/metrics")
def get_metrics():
    return {"calibration": calib_monitor.snapshot()}

@router.get("/state/ce")
def get_ce_state():
    signals = {"ensemble": {"signal": 0.0, "uncertainty": 0.5}}
    ce = CEState.from_signals(signals)
    C = ce.C
    if hasattr(C, "tolist"):
        C = C.tolist()
    return {"C": C, "dim": ce.meta.get("dim")}
