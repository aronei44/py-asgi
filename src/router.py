from src.exceptions import HTTPException


class Router:
    def __init__(self):
        self.routes = []
        self.ws_routes = {}

    def add(self, route):
        self.routes.append(route)

    def resolve(self, method, path):
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
        return None, None
    
    def add_websocket(self, path, handler):
        self.ws_routes[path] = handler

    def resolve_websocket(self, path):
        return self.ws_routes.get(path)
    
    def match_websocket(self, path: str):
        handler = self.ws_routes.get(path)
        if not handler:
            raise HTTPException("WebSocket route not found")
        return handler