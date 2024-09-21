import asyncio
from flowfunc.config import Config
from flowfunc.jobrunner import JobRunner
from flowfunc.exceptions import ErrorInDependentNode
from pathlib import Path
import json
from tests.methods import add_normal, add_async_with_sleep, divide_numbers

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

def test_run_add_async_return_coroutine():
    """JobRunner returns a coroutine"""
    nodes = json.loads(Path("tests/nodes_async.node").read_text())
    config = Config.from_function_list([add_async_with_sleep])
    runner = JobRunner(config, method="async")
    async_job = runner.run(nodes)
    results = asyncio.run(async_job)
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

def test_error_in_node():
    """Testing basic functionality"""
    nodes = json.loads(Path("tests/nodes_error.node").read_text())
    config = Config.from_function_list([divide_numbers])
    runner = JobRunner(config)
    results = runner.run(nodes)
    assert results
    assert results["node_1"].status == "failed"
    assert results["node_2"].status == "failed"
    assert type(results["node_2"].error) == ErrorInDependentNode


def test_run_add_async_dependent():
    """Testing basic functionality"""
    nodes = json.loads(Path("tests/nodes_async.node").read_text())
    assert len(nodes) == 5
    config = Config.from_function_list([add_async_with_sleep])
    runner = JobRunner(config)
    results = runner.run(nodes, selected_node_ids=["node_5"])
    assert results
    assert isinstance(results, dict)
    assert len(results) == 3
    assert results["node_1"].result == 1 + 2 # 3
    assert results["node_1"].result_mapped == {"result": results["node_1"].result}
    assert results["node_3"].result == 4 + results["node_1"].result
    assert results["node_3"].result_mapped == {"result": results["node_3"].result}
    assert results["node_5"].result == results["node_1"].result + results["node_3"].result
    assert all([n.status == "finished" for n in results.values()])
