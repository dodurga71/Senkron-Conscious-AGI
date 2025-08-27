def test_mlflow_noop_smoke(monkeypatch):
    import importlib

    mod = importlib.import_module("tracking.mlflow_logger")
    # Güvenli taraf: bayrağı kapatıp çağrıların patlamadığını gör
    try:
        monkeypatch.setattr(mod, "MLFLOW_ENABLED", False, raising=False)
    except Exception:
        pass

    with mod.start_run("noop"):
        mod.log_metric("acc", 0.9)
        mod.log_param("seed", 42)
    mod.end_run()
