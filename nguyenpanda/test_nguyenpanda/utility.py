from time import time
from typing import Callable, Any


def performance(func: Callable):
    def clock(*args: Any, **kwargs: Any):
        start = time()
        value = func(*args, **kwargs)
        end = time()
        interval = end - start
        print(f"'{func.__name__}' function took {interval:.5f} second to execute!")

        return interval, value

    return clock
