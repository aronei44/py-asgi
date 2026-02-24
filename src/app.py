from .request import Request
from .response import Response
from .router import Router

class App:
    def __init__(self):
        self.router = Router()

    def route(self, method: str, path: str):
        def decorator(fn):
            self.router.add(method, path, fn)
            return fn
        return decorator

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request = Request(scope, receive)
        handler, path_params = self.router.match(
            request.method,
            request.path
        )

        if not handler:
            response = Response(b"Not Found", status=404)
        else:
            params = {}
            params.update(path_params or {})
            params.update(request.query_params)
            result = handler(**params)

            if hasattr(result, "__await__"):
                result = await result

            response = result

        await response.send(send)