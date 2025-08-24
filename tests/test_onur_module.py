from fastapi.testclient import TestClient
from apps.main_api import app

client = TestClient(app)

def test_onur_endpoints():
    r1 = client.get("/onur/state/ce")
    assert r1.status_code == 200
    js1 = r1.json()
    assert "C" in js1 and "dim" in js1

    r2 = client.get("/onur/forecasts/raw")
    assert r2.status_code == 200
    js2 = r2.json()
    assert "signals" in js2 and "f_info" in js2
