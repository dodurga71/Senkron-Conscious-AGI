from __future__ import annotations

import json
import pathlib
import time
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Any


@contextmanager
def telemetry_run(
    component: str,
    out_dir: str = "logs/telemetry",
    extra: dict[str, Any] | None = None,
):
    """
    Komponent bazlı ölçüm. JSONL'e şu alanlar yazılır:
    {ts, run_id, component, duration_sec, emissions_kg, extra}
    CodeCarbon yoksa emisyon None yazılır.
    """
    start = time.time()
    run_id = str(uuid.uuid4())
    tracker = None
    emissions = None

    try:
        from codecarbon import EmissionsTracker  # opsiyonel

        tracker = EmissionsTracker(log_level="error", measure_power_secs=1, offline=True)
        tracker.start()
    except Exception:
        tracker = None

    try:
        yield
    finally:
        if tracker:
            try:
                emissions = tracker.stop()
            except Exception:
                emissions = None

        duration = time.time() - start
        payload = {
            "ts": datetime.now(UTC).isoformat(),
            "run_id": run_id,
            "component": component,
            "duration_sec": round(duration, 6),
            "emissions_kg": (float(emissions) if isinstance(emissions, int | float) else None),
            "extra": extra or {},
        }
        path = pathlib.Path(out_dir)
        path.mkdir(parents=True, exist_ok=True)
        fp = path / f"{datetime.utcnow().date()}.jsonl"
        with open(fp, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
