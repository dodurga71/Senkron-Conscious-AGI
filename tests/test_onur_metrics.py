from fastapi.testclient import TestClient
from apps.main_api import app

def test_onur_metrics_endpoint_accumulates():
    client = TestClient(app)
    r = client.post("/forecast/interpret", json={"features": {"momentum": 0.1}})
    assert r.status_code == 200
    r2 = client.get("/onur/metrics")
    assert r2.status_code == 200
    snap = r2.json().get("calibration", {})
    assert isinstance(snap.get("n"), int) and snap.get("n") >= 1
