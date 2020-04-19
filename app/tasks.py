import functools
import os
from time import sleep

import celery

CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

app = celery.Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


def fib(n):
    if n < 0:
        return []
    elif n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        results = fib(n - 1)
        results.append(results[-1] + results[-2])
        return results


def delay(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        sleep(2)  # simulate slow computation
        return func(*args, **kwargs)

    return wrapped


fib_delayed = delay(fib)
fib_celery = app.task(fib_delayed)
