from fastapi.testclient import TestClient
from apps.main_api import app

client = TestClient(app)

def test_interpret_endpoint_ok():
    payload = {"features": {"momentum": 0.5, "moon_phase": "waxing", "lyapunov": 0.3, "quantum_corr": 0.2, "risk_index": 0.4}}
    r = client.post("/forecast/interpret", json=payload)
    assert r.status_code == 200
    js = r.json()
    assert "nlg" in js and "raw" in js and "meta" in js
    assert "narrative" in js["nlg"] and "confidence" in js["nlg"]
    assert all(k in js["raw"] for k in ["signal","uncertainty","reliability","f_info","ce_dim"])
