import asyncio


def set_global_exception_handler():
    """Allow for exception handling in event loop."""
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)
