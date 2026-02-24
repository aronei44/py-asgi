import inspect
import json

from src.websocket import WebSocket
from .request import Request
from .response import Response
from .router import Router
from .route import Route
from .middleware import error_middleware
from .depends import Depends, resolve_dependency
from .schema import BaseModel, ValidationError

class App:
    def __init__(self, debug=False):
        self.debug = debug
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
                values[name] = await resolve_dependency(
                    param.default.dependency,
                    request
                )
                continue
            if (
                isinstance(param.annotation, type)
                and issubclass(param.annotation, BaseModel)
            ):
                try:
                    data = await request.json()
                    values[name] = param.annotation(**data)
                except ValidationError as e:
                    return Response(
                        str(e).encode(),
                        status=e.status
                    )
                except json.JSONDecodeError as e:
                    return Response(
                        str(e).encode() if self.debug else b"Invalid JSON body",
                        status=400
                    )
                except Exception as e:
                    return Response(
                        str(e).encode(),
                        status=400
                    )
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
    
    def websocket(self, path):
        def decorator(fn):
            self.router.add_websocket(path, fn)
            return fn
        return decorator
    
    async def handle_websocket(self, scope, receive, send):
        event = await receive()
        if event["type"] != "websocket.connect":
            return

        ws = WebSocket(scope, receive, send)

        try:
            handler = self.router.match_websocket(scope["path"])
            await handler(ws)
        except Exception:
            await ws.close(1011)

    async def handle_http(self, scope, receive, send):
        request = Request(scope, receive)

        handler = self.handle_request
        for mw in reversed(self.middlewares):
            handler = mw(handler)

        response = await handler(request)
        await response.send(send)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            await self.handle_http(scope, receive, send)
        elif scope["type"] == 'websocket':
            await self.handle_websocket(scope, receive, send)
        else:
            return

    def include_router(self, router, prefix=""):
        self.router.include_router(router, prefix)