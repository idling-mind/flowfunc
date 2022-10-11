import asyncio
import json
from pathlib import Path
import time
from flowfunc.config import Config
from flowfunc.distributed import NodeJob, NodeQueue
from flowfunc.jobrunner import JobRunner
from flowfunc.models import Node, OutNode
from tests.methods import add_async_with_sleep, add_normal
from redis import Redis
from uuid import uuid4
import os

def test_add_sync_distributed():
    """Testing a distributed run"""
    config = Config.from_function_list([add_normal])
    connection = Redis()
    queue = NodeQueue(connection=connection)
    runner = JobRunner(config, method="distributed", default_queue=queue)
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    results = runner.run(nodes)
    time.sleep(2)
    assert results
    assert isinstance(results, dict)
    first_node = results["node_1"]
    assert isinstance(first_node, OutNode)
    assert hasattr(first_node, "job_id")
    job = NodeJob.fetch(first_node.job_id, connection=connection)
    assert job
    assert job.get_status() == "finished"
    assert job.result == 3
    assert job.result_mapped == {"result": 3}

def test_add_async_distributed():
    """Testing a distributed run"""
    config = Config.from_function_list([add_normal])
    connection = Redis()
    queue = NodeQueue(connection=connection)
    runner = JobRunner(config, method="async_distributed", default_queue=queue)
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    async_job = runner.run(nodes)
    results =asyncio.run(async_job)
    time.sleep(1)
    assert results
    assert isinstance(results, dict)
    first_node = results["node_1"]
    assert isinstance(first_node, OutNode)
    assert hasattr(first_node, "job_id")
    job = NodeJob.fetch(first_node.job_id, connection=connection)
    assert job
    assert job.get_status() == "finished"
    assert job.result == 3

def test_add_async_distributed_same_worker():
    """Testing a distributed run"""
    config = Config.from_function_list([add_normal])
    connection = Redis()
    queue = NodeQueue(connection=connection)
    runner = JobRunner(config, method="distributed", same_worker=True, default_queue=queue)
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    job = runner.run(nodes)
    time.sleep(1)
    results = job.result
    assert results
    assert isinstance(results, dict)
    first_node = OutNode(**results["node_1"])
    assert isinstance(first_node, OutNode)
    first_node.result == 3

def test_node_with_settings():
    """Testing passing job_kwargs as settings of the node"""
    config = Config.from_function_list([add_normal])
    connection = Redis()
    queue = NodeQueue(connection=connection)
    runner = JobRunner(config, method="distributed", default_queue=queue)
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    node = nodes["node_1"]
    custom_job_id = str(uuid4())
    node["settings"] = {"job_id": custom_job_id}
    results = runner.run(nodes)
    time.sleep(2)
    assert results
    assert isinstance(results, dict)
    # checking if there is a job really with the set id
    job = NodeJob.fetch(custom_job_id, connection=connection)
    assert job
    assert job.get_status() == "finished"
    assert job.result == 3