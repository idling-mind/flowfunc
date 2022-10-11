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