import asyncio


def thread_and_pid_str():
    import os
    import threading
    return threading.current_thread().name + " ///" + str(threading.get_ident()) + "/// pid: " + str(os.getpid())


class Device:
    def __init__(self, name, polling_interval=1):
        self.name = name
        self.polling_interval = polling_interval
        self._loop = asyncio.get_running_loop()
        self._task = self._loop.create_task(self._run())

    async def _run(self):
        while True:
            await asyncio.sleep(self.polling_interval)
            print(f"{self.name} tick - {thread_and_pid_str()}")

    def close(self):
        self._task.cancel()

    def __del__(self):
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.close()

    async def await_closed(self):
        await self._task


async def main():
    d = Device("device1")

    while True:
        await asyncio.sleep(5)
        print(f"Tick {thread_and_pid_str()}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # kick off loop run forever
    loop.run_until_complete(main())
    loop.close()
