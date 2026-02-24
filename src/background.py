import inspect

class BackgroundTask:
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    async def run(self):
        result = self.fn(*self.args, **self.kwargs)
        if inspect.isawaitable(result):
            await result