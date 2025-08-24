from data_pipelines.etl.runner import run_etl


def test_run_etl_creates_file(tmp_path):
    raw = [
        {
            "timestamp": "2025-01-01T00:00:00Z",
            "source": "finance",
            "value": 1.2,
            "meta": {"citation_count": 10, "verified_source": True},
        },
        {
            "timestamp": "2025-01-02T00:00:00Z",
            "source": "social",
            "value": -0.4,
            "meta": {"citation_count": 0, "verified_source": False},
        },
    ]
    out = run_etl(raw, out_dir=str(tmp_path))
    assert out["ok"] == 2 and out["err"] == 0
