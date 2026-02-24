from src.app import App
from src.depends import Depends
from src.exceptions import NotFound
from src.request import Request
from src.response import Response
from middleware import logger_middleware, timing_middleware, test_state_middleware, auth_middleware
from state import get_profile

app = App()
app.add_middleware(logger_middleware)
app.add_middleware(timing_middleware)
app.add_middleware(test_state_middleware)
app.add_middleware(auth_middleware)

@app.route("GET", "/")
async def index(request):
    return Response(b"Hello Router")

@app.route("POST", "/echo")
async def echo(request: Request):
    body = await request.body()
    return Response(body)

@app.route("GET", "/users/{id}")
async def get_users(id):
    if id != "1":
        raise NotFound("user not found")

    return Response(b"user 1")

@app.route("GET", "/search")
async def search(q, page="1"):
    msg = f"q={q}, page={page}"
    return Response(msg.encode())

@app.route("GET", "/state-test")
async def state_test():
    # request belum diinject ke handler param
    # kita baca langsung dari middleware effect via closure
    return Response(b"OK")

@app.route("GET", "/me")
async def me(profile=Depends(get_profile)):
    return Response(profile.encode())