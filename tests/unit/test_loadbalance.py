import os
import time
import pytest

from jina import Flow, Executor, requests
from jina.enums import SchedulerType
from tests import random_docs


class SlowWorker(Executor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # half of worker is slow
        self.is_slow = os.getpid() % 2 != 0

    @requests
    def craft(self, **kwargs):
        if self.is_slow:
            time.sleep(1)


@pytest.mark.slow
def test_lb():
    f = Flow(runtime='process').add(name='sw', uses='SlowWorker', shards=10)
    with f:
        f.index(inputs=random_docs(100), request_size=10)


@pytest.mark.slow
def test_roundrobin():
    f = Flow(runtime='process').add(
        name='sw', uses='SlowWorker', shards=10, scheduling=SchedulerType.ROUND_ROBIN
    )
    with f:
        f.index(inputs=random_docs(100), request_size=10)
