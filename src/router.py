from .route import Route
class Router:
    def __init__(self):
        self.routes = []

    def add(self, method, path, handler):
        self.routes.append(Route(method, path, handler))

    def match(self, method, path):
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
        return None, None