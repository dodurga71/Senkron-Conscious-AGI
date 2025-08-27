from layer2_eft_core import compute_CE, minimize_Finfo


def test_eft_api():
    ce = compute_CE({"a": 1, "b": 2})
    assert ce >= 0.0
    out = minimize_Finfo(expect_KR=ce, alpha=0.5, S_EE=1.0)
    assert "F_info" in out
