# Flowfunc Examples

## Additional requirements

To run these examples, you need to install couple of packages in addition to `flowfunc`.

```
pip install dash-bootstrap-components rq
```

## Usage.py

This example shows the basic usage of `flowfunc`.

To run, clone this repo and run the following

```
cd examples
python usage.py
```

## Usage_rq.py

Running `flowfunc` nodes in a distributed way using redis and rq. Look in to the
documentation of [python-rq](https://python-rq.org/]) to know more.

```
cd examples
python usage_rq.py
```

Start the worker as below from this folder.

```
rqworker --job-class=flowfunc.distributed.NodeJob --queue-class=flowfunc.distributed.NodeQueue
```

This method is going to be slow for simple functions because of the overhead of
communication between dash, worker and client for each function call.
But this will method gives a lot of new possibilities like being able to run
long running tasks, shared results between different runs (because the only
thing another flow run needs to know is the job id to retrieve that result),
scheduled tasks (using the scheduler feature of python-rq), retries, etc.

I am hoping to add more examples later.