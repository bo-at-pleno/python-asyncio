import asyncio
import logging
import os
import random
import time
from functools import partial, wraps
from typing import Callable

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  [%(levelname)s]\t(%(process)d/%(thread)d)\t%(message)s')


def async_wrap(func: Callable) -> Callable:
    """Wrap a function to be called asynchronously.

    Args:
        func (_type_): standard function to be wrapped

    Returns:
        _type_: wrapped function
    """
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


@async_wrap
def slow_hello(name: str):
    import threading
    logging.info("wrapped hello:")
    logging.info("slow hello")
    random_delay = random.randint(1, 5)
    time.sleep(random_delay)
    logging.info("slow world")


async def hello():
    import threading
    logging.info("async hello")
    logging.info("Hello")
    await asyncio.sleep(1)
    logging.info("World")


async def main():
    print("In main:")
    await asyncio.gather(hello(), slow_hello("Bo"), slow_hello("Tom"), slow_hello("Jason"))

if __name__ == '__main__':
    asyncio.run(main())
