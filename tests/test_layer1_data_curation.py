from layer1_prediction_engine import curate_data, fuse_data


def test_curate_and_fuse():
    raw = [{"id": "e1", "ts": "2025-01-01", "x": 1}, {"id": "bad"}, None]  # elenmeli
    curated = curate_data(raw)
    assert len(curated) == 1
    fused = fuse_data(curated, astro={"a": 1}, finance={"b": 2})
    assert fused["fused"] is True
    assert fused["count"] == 1
    assert fused["has_astro"] and fused["has_finance"]
