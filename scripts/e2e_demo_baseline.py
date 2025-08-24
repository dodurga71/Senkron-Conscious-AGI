"""
e2e demo (güncel):
- Ham örnek veriyi oku
- Küratörlük + füzyon
- EFT C_E (kovaryans varsa Frobenius norm) ve F_info
- Narrative üret
- Metrik/enerji ölç ve JSON çıktı olarak kaydet
"""

import json
from pathlib import Path

from layer1_prediction_engine import curate_data, fuse_data
from layer2_eft_core import compute_CE, minimize_Finfo
from layer3_communication import generate_narrative
from layer4_test_validation import compute_accuracy, measure_energy_usage


def main():
    samples = Path("data_pipelines/samples/raw_events_min.json")
    raw = json.loads(samples.read_text(encoding="utf-8"))

    curated = curate_data(raw)
    fused = fuse_data(curated, astro={"ok": True}, finance={"ok": True})

    # Kovaryans örneği (2x2 birim matris -> Frobenius norm = sqrt(2))
    cov = [[1.0, 0.0], [0.0, 1.0]]
    ce = compute_CE({"cov": cov, "fused_count": fused["count"]})
    finfo = minimize_Finfo(expect_KR=ce, alpha=0.1, S_EE=1.0)

    narrative = generate_narrative({"topic": "demo", "score": finfo["F_info"]})
    acc = compute_accuracy([1, 0, 1], [1, 1, 1])
    energy = measure_energy_usage()

    out = {
        "curated_count": len(curated),
        "fused": fused,
        "C_E": ce,
        "F_info": finfo["F_info"],
        "narrative": narrative,
        "accuracy": acc,
        "energy": energy,
    }

    Path("outputs").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    Path("outputs/e2e_baseline.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[e2e-baseline] outputs/e2e_baseline.json yazıldı.")


if __name__ == "__main__":
    main()
