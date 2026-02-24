from src.app import App
from src.response import Response
from middleware import logger_middleware, timing_middleware

app = App()
app.add_middleware(logger_middleware)
app.add_middleware(timing_middleware)

@app.route("GET", "/")
async def index(request):
    return Response(b"Hello Router")

@app.route("POST", "/echo")
async def echo(request):
    body = await request.body()
    return Response(body)

@app.route("GET", "/users/{id}")
async def get_user(id):
    return Response(f"user id = {id}".encode())

@app.route("GET", "/search")
async def search(q, page="1"):
    msg = f"q={q}, page={page}"
    return Response(msg.encode())