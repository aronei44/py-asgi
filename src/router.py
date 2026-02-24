class Router:
    def __init__(self):
        self.routes = {}

    def add(self, method: str, path: str, handler):
        key = (method.upper(), path)
        self.routes[key] = handler

    def match(self, method: str, path: str):
        return self.routes.get((method.upper(), path))