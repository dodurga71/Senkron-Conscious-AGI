from layer2_eft_core import grid_minimize_finfo


def test_grid_minimize_positive_SEE():
    res = grid_minimize_finfo(expect_KR=1.0, S_EE=2.0, alphas=[0.0, 0.5, 1.0])
    assert res["alpha"] == 1.0  # S_EE>0 iken min için alpha en büyük


def test_grid_minimize_negative_SEE():
    res = grid_minimize_finfo(expect_KR=1.0, S_EE=-2.0, alphas=[0.0, 0.5, 1.0])
    assert res["alpha"] == 0.0  # S_EE<0 iken min için alpha en küçük
