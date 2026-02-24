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
            "headers": [
                (b"content-length", str(len(self.body)).encode()),
                (b"content-type", b"text/plain"),
            ] + self.headers
        })
        await send({
            "type": "http.response.body",
            "body": self.body,
            "more_body": False
        })
        if self.background:
            await self.background.run()