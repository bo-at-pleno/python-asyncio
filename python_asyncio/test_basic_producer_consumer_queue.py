import asyncio


async def hello():
    while True:
        logging.info("Hello")
        await asyncio.sleep(10)


async def main():
    queue = asyncio.Queue()
    # this will loop until the exception is raised
    await asyncio.gather(producer(queue), consumer(queue), hello())


async def producer(queue):
    i = 0
    while True:
        logging.info("Producing {}".format(i))
        queue.put_nowait(i)
        await asyncio.sleep(1)
        i += 1
        if i == 5:
            raise Exception("I'm done")


async def producer(queue):
    i = 0
    while True:
        logging.info("Producing {}".format(i))
        queue.put_nowait(i)
        await asyncio.sleep(1)
        i += 1
        if i == 5:
            raise Exception("I'm done")


async def consumer(queue):
    while True:
        logging.info("Consuming {}".format(await queue.get()))
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
