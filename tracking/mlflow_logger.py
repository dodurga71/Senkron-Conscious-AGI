from __future__ import annotations

from typing import Any

mlflow: Any = None
try:
    import mlflow as _mlflow  # type: ignore[import-not-found]

    mlflow = _mlflow
except Exception:
    mlflow = None
"""
MLflow skinny varsa kullan, yoksa no-op olacak hafif bir sarmalayıcı.
CI ve lokal testlerde import hatası atmadan log çağrılarını karşılar.
"""
try:
    import mlflow as _mlflow  # type: ignore[import-not-found]

    mlflow = _mlflow
except Exception:
    mlflow = None
    mlflow = None


class _NoopRun:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def start_run(run_name: str | None = None):
    if MLFLOW_ENABLED:
        return mlflow.start_run(run_name=run_name)
    return _NoopRun()


def end_run(status: str = "FINISHED"):
    if MLFLOW_ENABLED:
        try:
            mlflow.end_run(status=status)
        except Exception:
            pass  # sessizce yut


def log_metric(key: str, value: float, step: int | None = None):
    """CI'nin beklediği imza: tek metrik loglama."""
    if MLFLOW_ENABLED:
        try:
            mlflow.log_metric(key, float(value), step=step)
        except Exception:
            pass


def log_param(key: str, value: Any):
    if MLFLOW_ENABLED:
        try:
            mlflow.log_param(key, value)
        except Exception:
            pass


__all__ = ["start_run", "end_run", "log_metric", "log_param"]
MLFLOW_ENABLED: bool = mlflow is not None
