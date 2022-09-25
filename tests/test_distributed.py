import asyncio
import json
from pathlib import Path
import time
from fakeredis import FakeStrictRedis
from dash_flume.config import Config
from dash_flume.distributed import NodeJob, NodeQueue
from dash_flume.jobrunner import JobRunner
from dash_flume.models import Node, OutNode
from tests.methods import add_async_with_sleep, add_normal
from redis import Redis
import os

def test_add_sync_distributed():
    """Testing a distributed run"""
    config = Config.from_function_list([add_normal])
    connection = FakeStrictRedis()
    queue = NodeQueue(is_async=False, connection=connection)
    runner = JobRunner(config, method="distributed", default_queue=queue)
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    results = runner.run(nodes)
    assert results
    assert isinstance(results, dict)
    first_node = results["node_1"]
    assert isinstance(first_node, OutNode)
    assert hasattr(first_node, "job_id")
    job = NodeJob.fetch(first_node.job_id, connection=connection)
    assert job
    assert job.get_status() == "finished"
    assert job.result == 3

def test_add_async_distributed():
    """Testing a distributed run"""
    config = Config.from_function_list([add_normal])
    connection = FakeStrictRedis()
    queue = NodeQueue(connection=connection, is_async=False)
    runner = JobRunner(config, method="async_distributed", default_queue=queue)
    nodes = json.loads(Path("tests/nodes_add.node").read_text())
    async_job = runner.run(nodes)
    results =asyncio.run(async_job)

    assert results
    assert isinstance(results, dict)
    first_node = results["node_1"]
    assert isinstance(first_node, OutNode)
    assert hasattr(first_node, "job_id")
    job = NodeJob.fetch(first_node.job_id, connection=connection)
    assert job
    assert job.get_status() == "finished"
    assert job.result == 3
