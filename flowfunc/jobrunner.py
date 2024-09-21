from __future__ import annotations
import asyncio
import inspect
from copy import copy, deepcopy
from typing import Any, Callable, Dict, List, Optional

from pydantic import validate_call, ConfigDict

from .config import Config
from .exceptions import ErrorInDependentNode, QueueError
from .models import OutNode
from .utils import logger

try:
    from .distributed import NodeQueue
except ImportError:
    # Not opted for distributed
    pass


def default_meta_method(
    method,
    job_queue,
    job_runner,
    input_args,
    node,
    dependents,
    job_kwargs,
):
    """The default enqueuing method

    Parameters
    ----------
    method: Callable
        The function that should be submitted to the queue
    job_queue: NodeQueue
        The NodeQueue instance which should be used to submit the job
    input_args: dict
        The kwargs of method
    node: OutNode
        The pydantic node object
    config: Config
        Instance of the Config object which contains all the node functions
    dependents: List[str]
        List of dependent job IDs
    job_kwargs: dict
        Dict of keyword arguments for the rq enqueue function

    Returns
    -------
    job: NodeJob
        An instance of the rq job
    """
    return job_queue.enqueue(
        method,
        kwargs=input_args,  # this is later updated by the custom job class
        meta={
            "node_connections": node.connections.dict(),
            "result_keys": [
                x.name for x in job_runner.flume_config.get_node(node.type).outputs
            ],
            "node_id": node.id,
            **job_runner.meta_data,
        },
        depends_on=[dependent.job_id for dependent in dependents],
        **job_kwargs,
    )


def run_in_same_worker(flume_config, out_dict):
    """Run the whole flow in the same worker"""
    runner = JobRunner(flume_config=flume_config)
    result = {}
    run_output = runner.run(out_dict)
    if not run_output or not isinstance(run_output, dict):
        return result
    for nodeid, node in run_output.items():
        result[nodeid] = node.model_dump(exclude={"job", "run_event", "settings"})
        # Converting results to hashable type
        node_error = result[nodeid]["error"]
        if node_error:
            result[nodeid]["error"] = str(node_error)
    return result


class JobRunner:
    """Class which runs the flow

    Initiate an instance of this class with the config information. This instance
    can be used to run a flow dict which uses the nodes from the provided config.

    Use the 'run' method of this object to run the flow.

    Attributes
    ----------
    flume_config: Config
        The config object which contains all the nodes required to run the
        flow.
    method: str
        The way the JobRunner object should process the flow. There are three
        options as of now.
        sync: Synchronous, blocking run. If there are nodes which are async
            functions, they will be run asynchronously.
        async: Returns an awaitable when run
        distributed: Runs using python-rq. When run, returns the input dict, but
            updated with corresponding job objects for each node.
    default_queue: NodeQueue
        Required if the method is 'distributed'. default_queue is instance of
        NodeQueue class. If each node does not have a queue setting defined,
        this queue will be used.
    meta_map: Dict[Callable, Callable]
        Optional. A dictionary which matches the node function to a meta function.
        The meta function is responsible for enqueuing the job using the queue.
        Meta function gives better control in scheduling the job and use features
        from the python-rq library. Look at the default_meta_method to see how
        job is enqueued by default.
    meta_data: Dict[Any, Any]
        Optional. Any extra meta data to supply to the job
    """

    def __init__(
        self,
        flume_config: Config,
        method: str = "sync",
        same_worker: bool = False,
        # default_queue should be a NodeQueue instance but cannot annotate with
        # NodeQueue since it will make python-rq a required dependency
        default_queue: Optional[Any] = None,
        meta_map: Optional[Dict[Callable, Callable]] = None,
        meta_data: Optional[Dict[str, Any]] = None,
    ):
        self.flume_config = flume_config
        self.method = method
        self.queue = default_queue
        self.meta_map = meta_map if meta_map else {}
        self.meta_data = meta_data if meta_data else {}
        if self.method == "distributed" and self.queue is None:
            raise QueueError(
                "If the method is distributed, the `default_queue` argument cannot be empty."
            )
        self.same_worker = same_worker

    @validate_call
    def run(
        self,
        out_dict: Dict[str, OutNode],
        selected_node_ids: Optional[List[str]] = None,
    ):
        """Run the node map

        Parameters
        ----------
        out_dict: dict
            The output from the UI
        selected_nodes: List[str]
            The selected node IDs which should be run. The dependent nodes will
            automatically be identified from the out_dict and add to the list
            of nodes to be run.

        Returns
        -------
        mapped_dict: dict
            UI output dict converted to a dict with mapped pydantic OutNode objects
            for each node dictionary. Also, the results
            (if method is 'sync' or 'async') or job object (if method is
            'distributed') is attached to the Node.
        """
        if not out_dict:
            return
        mapped_dict = deepcopy(out_dict)
        if selected_node_ids:
            logger.info(
                f"Running {len(selected_node_ids)} node(s) out of {len(mapped_dict)}"
                f" in {self.method} mode."
            )
            dependent_node_ids = self.dependent_nodes(selected_node_ids, mapped_dict)
            logger.info(
                f"Found {len(dependent_node_ids)} nodes dependent on selected nodes."
            )
            mapped_dict = {nodeid: mapped_dict[nodeid] for nodeid in dependent_node_ids}
        else:
            logger.info(f"Running {len(mapped_dict)} nodes in {self.method} mode.")
        if self.method == "sync":
            return asyncio.run(self.run_async(mapped_dict))
        elif self.method == "async":
            return self.run_async(mapped_dict)
        elif self.method == "distributed" and self.same_worker:
            return asyncio.run(self.run_distributed_same_worker(out_dict))
        elif self.method == "async_distributed" and self.same_worker:
            return self.run_distributed_same_worker(out_dict)
        elif self.method == "distributed":
            return asyncio.run(self.run_distributed(mapped_dict))
        elif self.method == "async_distributed":
            return self.run_distributed(mapped_dict)
        else:
            raise ValueError(
                "The provided method is not identified."
                " It should be one of sync, async or distributed"
            )

    def dependent_nodes(self, selected_node_ids, mapped_dict):
        """Function to downselect only some nodes from the mapped_dict"""
        new_node_ids = []
        for nodeid, node in mapped_dict.items():
            if nodeid in selected_node_ids:
                new_node_ids.append(nodeid)
                if not node.connections.inputs:
                    continue
                for param, mapping in node.connections.inputs.items():
                    for connection in mapping:
                        new_node_ids.append(connection.nodeId)
        new_node_ids = list(set(new_node_ids))  # List of unique
        if len(new_node_ids) > len(selected_node_ids):
            return self.dependent_nodes(new_node_ids, mapped_dict)
        return new_node_ids

    async def run_async(self, mapped_dict) -> Dict[str, OutNode]:
        """Run the flow asynchronously"""
        nodes_evaluted = []
        for nodeid, node in mapped_dict.items():
            # Storing the lock in the node itself so that dependent nodes
            # dont start a new job.
            node.run_event = asyncio.Event()
            nodes_evaluted.append(self.evaluate_node_async(nodeid, mapped_dict))
        await asyncio.gather(*nodes_evaluted)
        return mapped_dict

    async def evaluate_node_async(self, nodeid: str, mapped_dict: dict):
        """Evaluate the node and return the result"""
        out_node = mapped_dict[nodeid]
        out_node.status = "started"
        if hasattr(out_node, "result") and out_node.result:
            return
        config_node = self.flume_config.get_node(out_node.type)
        # method = validate_arguments(config_node.method)
        method = config_node.method
        logger.info(f"Evaluating node with id {nodeid} and function {method}")
        out_node.result = None
        out_node.result_mapped = {}
        input_args = {}
        for key, values in out_node.inputData.items():
            if not values:
                continue
            # If there are more than one control in this port return the dict
            if len(values) > 1:
                variable_value = values
            else:
                # else return the value of the first item in the dict
                # TODO: when flume implements option to have multiple inputs
                # address it here.
                variable_value = next(iter(values.values()))
            if variable_value is None:
                continue  # This is null coming from react for unset controls
            input_args[key] = variable_value
        for key, connections in out_node.connections.inputs.items():
            # Now only one connection is supported by flume.
            # Hence using the first one
            dependent_nodeid = connections[0].nodeId
            dependent_node = mapped_dict[dependent_nodeid]
            out_node.status = "deferred"
            logger.info(f"Node {nodeid} waiting for Node {dependent_nodeid} to finish.")
            await dependent_node.run_event.wait()
            if hasattr(dependent_node, "error") and dependent_node.error:
                out_node.error = ErrorInDependentNode(
                    f"Error in node {dependent_node.id}"
                )
                out_node.status = "failed"
                out_node.run_event.set()
                return
            input_args[key] = dependent_node.result_mapped[connections[0].portName]
        if inspect.iscoroutinefunction(method):
            try:
                method_output = await validate_call(
                    config=ConfigDict(arbitrary_types_allowed=True)
                )(method)(**input_args)
            except Exception as e:
                out_node.error = e
                out_node.status = "failed"
        else:
            try:
                method_output = validate_call(
                    config=ConfigDict(arbitrary_types_allowed=True)
                )(method)(**input_args)
            except Exception as e:
                logger.error(f"Execution of Node {nodeid} has failed.")
                out_node.error = e
                out_node.status = "failed"
        out_node.run_event.set()

        if hasattr(out_node, "error") and out_node.error:
            return
        out_node.result = method_output

        # Converting the method output to a tuple so that it can be mapped
        # to the outputs dict
        if not isinstance(method_output, tuple):
            method_output = (method_output,)
        output_args = [
            x.name for x in (self.flume_config.get_node(out_node.type).outputs or [])
        ]
        out_node.result_mapped = {x: y for x, y in zip(output_args, method_output)}
        out_node.status = "finished"

    async def run_distributed(
        self, mapped_dict: Dict[str, OutNode]
    ) -> Dict[str, OutNode]:
        """Run the flow using python rq"""
        nodes_evaluted = []
        for nodeid, node in mapped_dict.items():
            # Storing the lock in the node itself so that dependent nodes
            # dont start a new job.
            if not hasattr(node, "run_event") or not node.run_event:
                node.run_event = asyncio.Event()
            nodes_evaluted.append(self.submit_node_job(nodeid, mapped_dict))
        await asyncio.gather(*nodes_evaluted)
        return mapped_dict

    async def run_distributed_same_worker(self, out_dict: dict) -> Dict[str, OutNode]:
        """Run the whole flow in the same worker using python-rq"""
        if (
            not hasattr(self, "queue")
            or not self.queue
            or not isinstance(self.queue, NodeQueue)
        ):
            raise QueueError(
                "If the method is distributed, the `default_queue` argument cannot be empty."
                " It should be an instance of NodeQueue."
            )
        return self.queue.enqueue(
            run_in_same_worker,
            kwargs={
                "flume_config": self.flume_config,
                "out_dict": out_dict,
            },
        )

    async def submit_node_job(self, nodeid: str, mapped_dict: dict):
        """Enqueue the node in the queue"""
        node = mapped_dict[nodeid]
        if hasattr(node, "job_id") and node.job_id:
            try:
                node.run_event.set()
            except Exception:
                pass
            return
        method = self.flume_config.get_node(node.type).method
        input_args = {}
        for key, values in node.inputData.items():
            if not values:
                continue
            # TODO: when flume implements multiple inputs for a node, address
            # it here
            variable_value = next(iter(values.values()))
            if variable_value is None:
                continue  # This is null coming from react
            input_args[key] = variable_value
        dependents = []
        for key, connections in node.connections.inputs.items():
            # Now only one connection is supported by flume.
            # Hence using the first one
            dependent_nodeid = connections[0].nodeId
            dependent_node = mapped_dict[dependent_nodeid]
            logger.info(
                f"Node {nodeid} waiting for Node {dependent_nodeid} to be submitted."
            )
            await dependent_node.run_event.wait()
            connections[0].job_id = dependent_node.job_id
            dependents.append(dependent_node)

        if hasattr(node, "settings") and isinstance(node.settings, dict):
            job_kwargs = copy(node.settings)
        else:
            job_kwargs = {}
        job_queue = job_kwargs.pop("queue", self.queue)
        depends_on = job_kwargs.pop("depends_on", [])
        try:
            dependents += depends_on
        except TypeError:
            dependents.append(depends_on)

        meta_method = self.meta_map.get(method, default_meta_method)

        node.job = meta_method(
            method,
            job_queue,
            job_runner=self,
            input_args=input_args,
            node=node,
            dependents=dependents,
            job_kwargs=job_kwargs,
        )
        logger.info(f"Node {nodeid} has been submitted.")
        node.job_id = node.job.id
        # Setting the current job's output connection job id
        # This may not be required
        if node.connections.outputs:
            for key, conns in node.connections.outputs.items():
                for conn in conns:
                    conn.job_id = node.job.id
        node.run_event.set()

    def dict(self, mapped_dict: Dict[str, OutNode], *args, **kwargs) -> dict:
        ret_dict = {}
        for nodeid, node in mapped_dict.items():
            ret_dict[nodeid] = node.model_dump(*args, **kwargs)
        return ret_dict
