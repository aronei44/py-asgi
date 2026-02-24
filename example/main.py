from example.router import router
from src.app import App

from example.middleware import logger_middleware, timing_middleware, test_state_middleware, auth_middleware

app = App()
app.add_middleware(logger_middleware)
app.add_middleware(timing_middleware)
app.add_middleware(test_state_middleware)
app.add_middleware(auth_middleware)

app.include_router(router, prefix="")


@app.websocket("/ws")
async def ws_handler(ws):
    await ws.accept()

    while True:
        msg = await ws.receive_text()
        if msg is None:
            break
        await ws.send_text(f"echo: {msg}")