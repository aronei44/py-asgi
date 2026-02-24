import re

class Route:
    def __init__(self, method, path, handler):
        self.method = method.upper()
        self.path = path
        self.handler = handler
        self.param_names = []

        pattern = "^"
        for part in path.strip("/").split("/"):
            if part.startswith("{") and part.endswith("}"):
                name = part[1:-1]
                self.param_names.append(name)
                pattern += r"/(?P<%s>[^/]+)" % name
            else:
                pattern += f"/{part}"
        pattern += "$"

        self.regex = re.compile(pattern)

    def match(self, method, path):
        if method.upper() != self.method:
            return None
        match = self.regex.match(path)
        if not match:
            return None
        return match.groupdict()