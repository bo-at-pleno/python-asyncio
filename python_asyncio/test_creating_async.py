import asyncio
import logging
from typing import Coroutine

logging.basicConfig(level=logging.DEBUG)


def thread_and_pid_str():
    import os
    import threading
    return "[tid: " + threading.current_thread().name + "/" + str(threading.get_ident()) + ", pid: " + str(os.getpid()) + "]"


class Device:
    def __init__(self, name, polling_interval=1):
        self.name = name
        self.polling_interval = polling_interval
        self._loop = asyncio.get_running_loop()
        # starts a task automaticallly
        self._polling_task = self._loop.create_task(self._poll())
        logging.info("Device created - " + thread_and_pid_str())
        logging.info(" Task: " + str(self._polling_task) +
                     " - " + thread_and_pid_str())

    async def _poll(self):
        """Runs forever, polling the device for data."""
        while True:
            await asyncio.sleep(self.polling_interval)
            logging.info(f"{self.name} tick - {thread_and_pid_str()}")

    def get_async_task(self) -> Coroutine:
        async def slow_async_task():
            logging.info("Launching slow task, device name: " +
                         self.name + " - " + thread_and_pid_str())
            await asyncio.sleep(5)
            logging.info(
                "Slow async task from device {} finished".format(self.name))
        return slow_async_task

    def close(self):
        self._polling_task.cancel()

    def __del__(self):
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()

    async def await_closed(self):
        await self._polling_task


async def main():
    d = Device("device1")
    i = 0

    _loop = asyncio.get_running_loop()
    # starts a task automaticallly
    running_tasks = []
    while True:
        logging.info("Main loop {} - {}".format(i, thread_and_pid_str()))
        i += 1
        # kick off a slow device task every 5 ticks
        if i % 3 == 1:
            tsk = d.get_async_task()
            running_tasks.append(_loop.create_task(tsk()))

        for tsk in running_tasks:
            if tsk.done():
                logging.info(
                    "Main loop detected task {} done - {}".format(tsk, thread_and_pid_str()))
                running_tasks.remove(tsk)

        await asyncio.sleep(2)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # kick off loop run forever
    loop.run_until_complete(main())
    loop.close()
