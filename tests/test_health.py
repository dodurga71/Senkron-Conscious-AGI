from fastapi.testclient import TestClient
from apps.main_api import app

client = TestClient(app)

def test_healthz():
    r = client.get('/healthz')
    assert r.status_code == 200
    js = r.json()
    assert js.get("ok") is True
