"""
Basit e2e demo (iskele):
- Ham örnek veriyi oku
- Küratörlük + füzyon
- EFT C_E ve F_info (placeholder)
- Narrative üret
- Metrik/enerji ölç ve yazdır
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

    ce = compute_CE({"example": 1, "fused_count": fused["count"]})
    finfo = minimize_Finfo(expect_KR=ce, alpha=0.1, S_EE=1.0)

    narrative = generate_narrative({"topic": "demo", "score": finfo["F_info"]})
    acc = compute_accuracy([1, 0, 1], [1, 1, 1])
    energy = measure_energy_usage()

    print("CURATED:", len(curated))
    print("FUSED :", fused)
    print("C_E   :", ce)
    print("F_info:", finfo)
    print("NLG   :", narrative)
    print("ACC   :", acc)
    print("ENERGY:", energy)


if __name__ == "__main__":
    main()
