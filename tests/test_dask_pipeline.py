from data_pipelines.dask_pipeline import load_json_array


def test_dask_load_json_array():
    rows = load_json_array("data_pipelines/samples/raw_events_min.json")
    assert isinstance(rows, list)
    assert len(rows) == 2  # üçüncü kayıt (bad) elenmeli
