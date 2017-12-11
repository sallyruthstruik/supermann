from multiprocessing.pool import Pool

import psutil
import pytest

from supermann.metrics.process import with_children


@pytest.fixture()
def process():
    #create process pull
    pool = Pool(5)
    return psutil.Process()

def test_with_children(process):
    #type: (psutil.Process)->None
    assert len(process.children()) == 5

    assert with_children(process, lambda p: p.memory_info().rss) > process.memory_info().rss
