class WebSocket:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self._receive = receive
        self._send = send

    async def accept(self):
        await self._send({
            "type": "websocket.accept"
        })

    async def close(self, code=1000):
        await self._send({
            "type": "websocket.close",
            "code": code
        })

    async def receive(self):
        return await self._receive()

    async def receive_text(self):
        event = await self._receive()

        if event["type"] == "websocket.receive":
            return event.get("text")

        if event["type"] == "websocket.disconnect":
            return None

    async def send_text(self, text: str):
        await self._send({
            "type": "websocket.send",
            "text": text
        })