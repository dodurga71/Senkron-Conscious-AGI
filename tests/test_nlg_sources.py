from fastapi.testclient import TestClient

from apps.main_api import app

client = TestClient(app)


def test_interpret_includes_sources():
    r = client.post(
        "/forecast/interpret", json={"features": {"momentum": 0.2, "risk_index": 0.4}}
    )
    assert r.status_code == 200
    js = r.json()
    assert "nlg" in js and "raw" in js
    assert isinstance(js["raw"].get("sources"), list)
    # nlg içinde kaynak özeti bulunmalı (boş da olabilir ama alan var)
    assert "source_summary" in js["nlg"]
