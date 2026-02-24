class Response:
    def __init__(self, body=b"", status=200, headers=None, background=None):
        self.body = body
        self.status = status
        self.headers = headers or []
        self.background = background

    async def send(self, send):
        await send({
            "type": "http.response.start",
            "status": self.status,
            "headers": self.headers,
        })
        await send({
            "type": "http.response.body",
            "body": self.body,
        })
        if self.background:
            await self.background.run()