from fastapi import APIRouter
from layer4_test_validation.calib_monitor import calib_monitor

router = APIRouter(prefix="/onur", tags=["onur"])

@router.get("/ping")
def ping():
    return {"ok": True}

@router.get("/metrics")
def get_metrics():
    return {"calibration": calib_monitor.snapshot()}
