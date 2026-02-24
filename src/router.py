from src.exceptions import HTTPException
from src.route import Route

class Router:
    def __init__(self, prefix=""):
        self.prefix = prefix.rstrip("/")
        self.routes = []
        self.ws_routes = {}
        self.middlewares = []

    def add(self, route):
        self.routes.append(route)

    def resolve(self, method, path):
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
        return None, None

    # ---------- middleware ----------
    def middleware(self, mw):
        self.middlewares.append(mw)
        return mw

    # ---------- websocket ----------
    def add_websocket(self, path, handler):
        self.ws_routes[path] = handler

    def match_websocket(self, path: str):
        handler = self.ws_routes.get(path)
        if not handler:
            raise HTTPException("WebSocket route not found")
        return handler

    # ---------- include router ----------
    def include_router(self, router, prefix=""):
        full_prefix = (self.prefix + prefix).rstrip("/")

        self.middlewares.extend(router.middlewares)

        for route in router.routes:
            new_path = full_prefix + route.path
            self.add(Route(route.method, new_path, route.handler))

    # ---------- decorators ----------
    def route(self, method, path):
        def decorator(fn):
            self.add(Route(method, path, fn))
            return fn
        return decorator

    def get(self, path):
        return self.route("GET", path)

    def post(self, path):
        return self.route("POST", path)

    def put(self, path):
        return self.route("PUT", path)

    def delete(self, path):
        return self.route("DELETE", path)