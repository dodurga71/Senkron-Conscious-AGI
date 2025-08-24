from __future__ import annotations
from typing import Dict, Any, Optional
import os

def log_run(run_name: str, params: Dict[str, Any], metrics: Dict[str, float], tags: Optional[Dict[str, Any]] = None) -> bool:
    """
    MLflow-skinny mevcut ve MLFLOW_LOG=1 ise loglar.
    Yoksa sessizce no-op (False döner).
    """
    if os.getenv("MLFLOW_LOG", "0") != "1":
        return False
    try:
        import mlflow
    except Exception:
        return False

    try:
        uri = os.getenv("MLFLOW_TRACKING_URI")
        if uri:
            mlflow.set_tracking_uri(uri)
        with mlflow.start_run(run_name=run_name):
            for k, v in (params or {}).items():
                mlflow.log_param(k, str(v))
            for k, v in (metrics or {}).items():
                try:
                    mlflow.log_metric(k, float(v))
                except Exception:
                    pass
            if tags:
                mlflow.set_tags(tags)
        return True
    except Exception:
        return False
