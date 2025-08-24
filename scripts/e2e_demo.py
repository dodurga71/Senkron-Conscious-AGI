from pathlib import Path
import json

from data_pipelines.etl.runner import run_etl
from telemetry.logger import telemetry_run
from fastapi.testclient import TestClient
from apps.main_api import app
from config.settings import get_settings

def main():
    settings = get_settings()
    samples_path = Path("data_pipelines/samples/raw_events.json")
    raw = json.loads(samples_path.read_text(encoding="utf-8-sig"))

    with telemetry_run("etl", out_dir=settings.TELEMETRY_DIR, extra={"dataset": "samples"}):
        out = run_etl(raw, out_dir=settings.OUTPUT_DIR)

    curated_path = Path(out["outfile"])
    curated = [json.loads(l) for l in curated_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    avg_val = sum(r["value"] for r in curated)/len(curated) if curated else 0.0
    features = {
        "momentum": avg_val, "moon_phase": "waxing",
        "lyapunov": 0.3, "quantum_corr": 0.1, "risk_index": 0.4
    }

    client = TestClient(app)
    with telemetry_run("inference_api", out_dir=settings.TELEMETRY_DIR, extra={"route": "/forecast/interpret"}):
        resp = client.post("/forecast/interpret", json={"features": features})
        resp.raise_for_status()
        js = resp.json()

    Path("outputs").mkdir(parents=True, exist_ok=True)
    report_path = Path("outputs/demo_report.json")
    report_path.write_text(json.dumps({"features": features, "api_response": js}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Demo OK ->", report_path)

if __name__ == "__main__":
    main()
