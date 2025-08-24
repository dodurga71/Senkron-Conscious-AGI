import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.main_api import app
from config.settings import get_settings
from data_pipelines.etl.runner import run_etl
from telemetry.logger import telemetry_run


def main() -> None:
    # Ortamı doğrula
    _ = get_settings()

    # Örnek veri (dosya JSON array; BOM olabilir)
    samples_path = Path("data_pipelines/samples/raw_events.json")
    raw_text = samples_path.read_text(encoding="utf-8-sig")
    raw_records = json.loads(raw_text)  # -> list[dict]

    # ETL
    out = run_etl(raw_records, out_dir="outputs")

    # Curated çıktıyı oku (JSONL)
    curated_path = Path(out["outfile"])
    curated = [json.loads(line) for line in curated_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    # Basit özellik: ortalama değer -> momentum
    avg_val = sum(r["value"] for r in curated) / len(curated) if curated else 0.0
    features = {"momentum": avg_val}

    # API çağrısı
    client = TestClient(app)
    r = client.post("/forecast/interpret", json={"features": features})
    r.raise_for_status()
    js = r.json()

    # Telemetry (şimdilik boş blok; istersen içine log koyarız)
    with telemetry_run("e2e_demo"):
        pass

    # Rapor yaz
    report_path = Path("outputs/demo_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(js, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Demo OK -> {report_path}")


if __name__ == "__main__":
    main()
