import asyncio
import random
import time


def make_random_async_task():
    random_delay = random.randint(1, 5)

    async def async_task():
        print("task start ({})".format(random_delay))
        await asyncio.sleep(random_delay)
        print("task end ({})".format(random_delay))

async def main(queue, output_queue):
    while True:
        task = await queue.get()

        if task is None:
            break

        print("Consuming {}".format(task))
        # execute async task
        task_res = await task
        output_queue.put_nowait(task_res)

async def result_consumer(queue):
    while True:
        task_res = await queue.get()

        if task_res is None:
            break

        print("result: {}".format(task_res))

if __name__ == '__main__':
    queue = asyncio.Queue()
    for i in range(10):
        queue.put_nowait(make_random_async_task())

    queue.put_nowait(None)
    output_queue = asyncio.Queue()

    asyncio.run(main(queue, output_queue))
