import pytest

from app import tasks

cases = [
    (-1, []),
    (1, [0, 1]),
    (3, [0, 1, 1, 2]),
    (5, [0, 1, 1, 2, 3, 5]),
]


@pytest.mark.parametrize("n, expected", cases)
def test_fib_task(monkeypatch, n, expected):
    monkeypatch.setattr(tasks.fib_celery, "run", tasks.fib)
    assert tasks.fib_celery.run(n) == expected
