from config.settings import Settings

def test_settings_env(monkeypatch):
    monkeypatch.setenv("TELEMETRY_DIR","tlog")
    s = Settings()
    assert s.TELEMETRY_DIR == "tlog"
