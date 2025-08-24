from fastapi import APIRouter
from collections import deque
from typing import Dict, Any, List, Optional
from layer4_test_validation.calib_monitor import calib_monitor
from layer2_eft_core.ce_state import CEState

router = APIRouter(prefix="/onur", tags=["onur"])

# In-memory ring buffer (son 1000 kayıt)
_FORECASTS_RAW: deque = deque(maxlen=1000)

def record_forecast_observation(raw: Dict[str, Any]) -> None:
    """/forecast/interpret çıktısının 'raw' kısmını hafızada sakla."""
    try:
        _FORECASTS_RAW.append(raw)
    except Exception:
        pass

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

@router.get("/forecasts/raw")
def get_forecasts_raw(limit: int = 20):
    """Son ham tahminler (interpret -> raw)."""
    items: List[Dict[str, Any]] = list(_FORECASTS_RAW)[-limit:]
    last: Optional[Dict[str, Any]] = items[-1] if items else None
    return {"count": len(_FORECASTS_RAW), "last": last, "items": items}
