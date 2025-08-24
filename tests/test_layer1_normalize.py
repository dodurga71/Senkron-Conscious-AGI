from layer1_prediction_engine import normalize_numeric_fields


def test_minmax_normalize_basic():
    rows = [{"id": "e1", "ts": "t", "payload_score": 10.0}, {"id": "e2", "ts": "t", "payload_score": 20.0}]
    out, stats = normalize_numeric_fields(rows, ["payload_score"])
    assert 0.0 <= out[0]["payload_score"] <= 1.0
    assert 0.0 <= out[1]["payload_score"] <= 1.0
    assert stats["payload_score"]["min"] == 10.0
    assert stats["payload_score"]["max"] == 20.0
