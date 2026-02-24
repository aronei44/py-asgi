import json
from urllib.parse import parse_qs
from .state import State

class Request:
    def __init__(self, scope, receive):
        self.scope = scope
        self._receive = receive
        self._body = None
        self.state = State()

    @property
    def method(self):
        return self.scope["method"]

    @property
    def path(self):
        return self.scope["path"]

    @property
    def query_params(self):
        raw = self.scope.get("query_string", b"")
        parsed = parse_qs(raw.decode())
        return {k: v[0] for k, v in parsed.items()}

    async def body(self):
        if self._body is None:
            chunks = []
            while True:
                event = await self._receive()
                if event["type"] != "http.request":
                    break
                chunks.append(event.get("body", b""))
                if not event.get("more_body", False):
                    break
            self._body = b"".join(chunks)
        return self._body
    
    async def json(self):
        body = await self.body()
        return json.loads(body.decode())