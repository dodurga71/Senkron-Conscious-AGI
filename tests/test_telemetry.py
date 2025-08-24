from telemetry.logger import telemetry_run
import json, os

def test_telemetry_writes(tmp_path):
    logdir = tmp_path / "tlog"
    with telemetry_run("unit_test", out_dir=str(logdir), extra={"k":"v"}):
        pass
    files = list(os.scandir(logdir))
    assert len(files) >= 1
