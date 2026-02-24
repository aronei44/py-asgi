from .request import Request
from .response import Response
from .router import Router
from .route import Route

class App:
    def __init__(self):
        self.router = Router()
        self.middlewares = []

    def route(self, method, path):
        def decorator(fn):
            route = Route(method, path, fn)
            self.router.add(route)
            return fn
        return decorator

    async def handle_request(self, request):
        handler, path_params = self.router.resolve(
            request.method,
            request.path
        )

        if not handler:
            return Response(b"Not Found", status=404)

        params = {}
        params.update(path_params or {})
        params.update(request.query_params)

        result = handler(**params)
        if hasattr(result, "__await__"):
            result = await result

        return result

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request = Request(scope, receive)

        handler = self.handle_request
        for mw in reversed(self.middlewares):
            handler = mw(handler)

        response = await handler(request)
        await response.send(send)