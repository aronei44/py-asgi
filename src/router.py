class Router:
    def __init__(self):
        self.routes = []

    def add(self, route):
        self.routes.append(route)

    def resolve(self, method, path):
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
        return None, None