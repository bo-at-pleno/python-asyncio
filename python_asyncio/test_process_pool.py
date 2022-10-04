import sys
from multiprocessing import pool


class Container:

    def __init__(self):
        self._pool = pool.Pool(4)
        self.configs = {"foo": "bar"}

    def run(self, param):
        self._pool.apply_async(self._run, (param,), kwds=self.configs)

    def wait(self):
        self._pool.close()
        self._pool.join()

    def shutdown(self):
        self._pool.terminate()

    @staticmethod
    def _run(param, **kwargs):
        print("hello world, param: {}, kwargs: {}".format(param, kwargs))


def main():
    c = Container()

    for i in range(10):
        c.run(i)
    c.wait()
    c.shutdown()


if __name__ == "__main__":
    sys.exit(main())
