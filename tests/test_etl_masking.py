from data_pipelines.etl.transformers import pii_mask, reliability_tagging


def test_pii_mask_basic():
    rec = {
        "email": "alice@example.com",
        "phone": "+90 555 123 45 67",
        "headline": "Haber başlığı",
    }
    out = pii_mask(rec, whitelist_keys={"headline"})
    assert out["email"] == "***" or "@" not in out["email"]
    assert out["headline"] == "Haber başlığı"


def test_reliability_tagging_bounds():
    s = reliability_tagging("finance", {"citation_count": 50, "verified_source": True})
    assert 0.0 <= s <= 1.0
