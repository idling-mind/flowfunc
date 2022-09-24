from dash_flume.config import Config
from dash_flume.jobrunner import JobRunner
from pathlib import Path
import json
from tests.methods import add_normal, add_async_with_sleep

def test_blank():
    """Testing if running empty dict will return empty output"""
    nodes = {}
    config = Config.from_function_list([add_normal])
    runner = JobRunner(config)
    results = runner.run(nodes)
    assert not results

def test_run_add():
    """Testing basic functionality"""
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    config = Config.from_function_list([add_normal])
    runner = JobRunner(config)
    results = runner.run(nodes)
    assert results
    assert isinstance(results, dict)
    assert len(results) == 5
    assert results["node_1"].result == 1 + 2 # 3
    assert results["node_1"].result_mapped == {"result": results["node_1"].result}
    assert results["node_2"].result == 3 + results["node_1"].result # 6
    assert results["node_2"].result_mapped == {"result": results["node_2"].result}
    assert results["node_3"].result == 4 + results["node_1"].result
    assert results["node_3"].result_mapped == {"result": results["node_3"].result}
    assert results["node_4"].result == results["node_2"].result + results["node_5"].result
    assert results["node_5"].result == results["node_1"].result + results["node_3"].result
    assert all([n.status == "finished" for n in results.values()])


def test_run_add_async():
    """Testing basic functionality"""
    nodes = json.loads(Path("tests/nodes_async.node").read_text())
    config = Config.from_function_list([add_async_with_sleep])
    runner = JobRunner(config)
    results = runner.run(nodes)
    assert results
    assert isinstance(results, dict)
    assert len(results) == 5
    assert results["node_1"].result == 1 + 2 # 3
    assert results["node_1"].result_mapped == {"result": results["node_1"].result}
    assert results["node_2"].result == 3 + results["node_1"].result # 6
    assert results["node_2"].result_mapped == {"result": results["node_2"].result}
    assert results["node_3"].result == 4 + results["node_1"].result
    assert results["node_3"].result_mapped == {"result": results["node_3"].result}
    assert results["node_4"].result == results["node_2"].result + results["node_5"].result
    assert results["node_5"].result == results["node_1"].result + results["node_3"].result
    assert all([n.status == "finished" for n in results.values()])