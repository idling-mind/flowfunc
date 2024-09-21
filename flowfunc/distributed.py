"""
RQ Utils
--------
This module defines redis-queue related classess and functions.
"""
from __future__ import annotations
from rq.job import Job
from rq.queue import Queue
from .models import OutConnections
from pydantic import validate_arguments


class NodeJob(Job):
    """Custom job class which will modify the kwargs based on the dependencies
    of the current job

    There should be two meta variables, node_connections and result_keys which
    will define the connections to the current node and the variable names of
    the output of the current node.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        node_connections = self.get_meta().get("node_connections")
        if node_connections:
            self.node_connections = OutConnections(**node_connections)
        else:
            self.node_connections = None
        # keys for the result dict
        self.result_keys = self.get_meta().get("result_keys", ["result"])

    def update_kwargs(self):
        if not self.node_connections or not self.node_connections.inputs:
            return
        for key, node_connection in self.node_connections.inputs.items():
            # Assuming dependent job shares the same connection.
            # Also, dependent job should be complete before this job starts peforming.
            # Also assuming that there is only one connection in one port
            # as flume allows only one at this time.
            dependent_job = NodeJob.fetch(
                node_connection[0].job_id, connection=self.connection
            )
            self.kwargs.update(
                {key: dependent_job.result_mapped[node_connection[0].portName]}
            )

    @property
    def func(self):
        """Overriding Job class' func method to include argument validation"""
        return validate_arguments(
            super().func, config=dict(arbitrary_types_allowed=True)
        )

    def perform(self):
        """Overriding the perform method of the parent class"""
        self.update_kwargs()
        return super().perform()

    @property
    def result_mapped(self):
        """Mapped result dictionary

        Creating an extra property which is a dictionary with keys equal to the
        output ports of the node.
        """
        res = self.result
        if not isinstance(res, tuple):
            # If there is only one result item and has to be converted
            # to a tuple to map it onto a dict and later to kwargs
            res = (res,)
        return {x: y for x, y in zip(self.result_keys, res)}


class NodeQueue(Queue):
    """Node Queue class is derived from the base Queue class in RQ"""

    job_class = NodeJob
