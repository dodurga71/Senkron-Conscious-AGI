from collections import deque
from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from layer2_eft_core.ce_state import CEState
from layer4_test_validation.calib_monitor import calib_monitor

router = APIRouter(prefix="/onur", tags=["onur"])

# In-memory ring buffer (son 1000 kayıt)
_FORECASTS_RAW: deque = deque(maxlen=1000)


def record_forecast_observation(raw: Dict[str, Any]) -> None:
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
    """
    Son ham tahminler (interpret -> raw).
    Test beklentisi: top-level 'signals' (liste) ve 'f_info' (son değer) alanları bulunsun.
    """
    items: List[Dict[str, Any]] = list(_FORECASTS_RAW)[-limit:]
    last: Optional[Dict[str, Any]] = items[-1] if items else None
    signals: List[float] = [float(x.get("signal", 0.0)) for x in items]
    f_info_last: Optional[float] = (
        float(last.get("f_info")) if (last and "f_info" in last) else None
    )
    return {
        "count": len(_FORECASTS_RAW),
        "signals": signals,  # <-- testin aradığı alan
        "f_info": f_info_last,  # <-- testin aradığı alan
        "last": last,
        "items": items,
    }
