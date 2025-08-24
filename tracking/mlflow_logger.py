from __future__ import annotations

from typing import Any, Optional

"""
MLflow skinny varsa kullan, yoksa no-op olacak hafif bir sarmalayıcı.
CI ve lokal testlerde import hatası atmadan log çağrılarını karşılar.
"""

MLFLOW_ENABLED = False
try:
    import mlflow  # type: ignore

    MLFLOW_ENABLED = True
except Exception:
    mlflow = None  # type: ignore[misc]


class _NoopRun:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def start_run(run_name: Optional[str] = None):
    if MLFLOW_ENABLED:
        return mlflow.start_run(run_name=run_name)  # type: ignore[attr-defined]
    return _NoopRun()


def end_run(status: str = "FINISHED"):
    if MLFLOW_ENABLED:
        try:
            mlflow.end_run(status=status)  # type: ignore[attr-defined]
        except Exception:
            pass  # sessizce yut


def log_metric(key: str, value: float, step: Optional[int] = None):
    """CI'nin beklediği imza: tek metrik loglama."""
    if MLFLOW_ENABLED:
        try:
            mlflow.log_metric(key, float(value), step=step)  # type: ignore[attr-defined]
        except Exception:
            pass


def log_param(key: str, value: Any):
    if MLFLOW_ENABLED:
        try:
            mlflow.log_param(key, value)  # type: ignore[attr-defined]
        except Exception:
            pass


__all__ = ["start_run", "end_run", "log_metric", "log_param"]
