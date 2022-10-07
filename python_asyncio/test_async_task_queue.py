import asyncio
import logging
import random
import time
from typing import Coroutine

logging.basicConfig()


def make_random_async_task(id: int) -> Coroutine:
    random_delay = random.randint(2, 8)

    async def async_task():
        logging.info("task start ({})".format(id))
        await asyncio.sleep(random_delay)
        logging.info("task complete!({})".format(id))
        return "task {} result, random wait was {}".format(id, random_delay)

    return async_task


async def executor(input_queue, output_queue):
    logging.info("Starting executor")
    while True:
        task = await input_queue.get()
        if task is None:
            logging.info("Got none, shutting down executor")
            output_queue.put_nowait(None)
            break

        logging.info("Executing {}".format(task))
        # execute async task
        task_res = await task()
        output_queue.put_nowait(task_res)


async def main(input_queue, output_queue):
    logging.info("In main, kicking off executor and consumer")
    for i in range(5):
        logging.info("adding task {} to input queue...".format(i))
        input_queue.put_nowait(make_random_async_task(i))

    # poison pill
    input_queue.put_nowait(None)

    await asyncio.gather(result_consumer(output_queue),
                         executor(input_queue, output_queue))


async def result_consumer(output_queue: asyncio.Queue):
    logging.info("Starting Result consumer")
    while True:
        task_res = await output_queue.get()

        if task_res is None:
            logging.info("Got None, shutting down consumer")
            break

        logging.info("result: {}".format(task_res))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # put stuff into queue ahead of time from a synchronous thread
    input_queue = asyncio.Queue(loop=loop)
    output_queue = asyncio.Queue(loop=loop)

    # input_queue.put_nowait(None)
    loop.run_until_complete(main(input_queue, output_queue))
