import inspect
from .request import Request
from .response import Response
from .router import Router
from .route import Route
from .middleware import error_middleware
from .depends import Depends

class App:
    def __init__(self):
        self.router = Router()
        self.middlewares = [
            error_middleware
        ]

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

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

        sig = inspect.signature(handler)
        values = {}

        for name, param in sig.parameters.items():

            if param.annotation is Request:
                values[name] = request
                continue

            if isinstance(param.default, Depends):
                dep = param.default.dependency
                dep_result = dep(request)

                if inspect.isawaitable(dep_result):
                    dep_result = await dep_result

                values[name] = dep_result
                continue

            if path_params and name in path_params:
                values[name] = path_params[name]
                continue

            if name in request.query_params:
                values[name] = request.query_params[name]

        result = handler(**values)

        if inspect.isawaitable(result):
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