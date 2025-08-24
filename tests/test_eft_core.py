from layer2_eft_core.ce_state import CEState
from layer2_eft_core.eft_objective import f_info

def test_ce_state_and_finfo():
    signals = {"a": {"signal": 0.1, "uncertainty": 0.3},
               "b": {"signal": 0.0, "uncertainty": 0.5}}
    ce = CEState.from_signals(signals)
    assert ce.C.shape[0] == ce.meta["dim"]
    score = f_info(signals, ce.C, alpha=0.1)
    assert isinstance(score, float)
