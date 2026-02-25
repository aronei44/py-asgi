from example.bg import send_email
from example.schema import UserIn
from example.state import get_profile
from src.background import BackgroundTask
from src.depends import Depends
from src.exceptions import HTTPException, NotFound
from src.request import Request
from src.response import Response
from src.router import Router


router = Router()

# route middleware
@router.middleware
async def auth(handler):
    print("🔥 DIPANGGIL")
    async def wrapped(req):
        return await handler(req)
        # contoh raisenya
        # raise HTTPException(status=401,detail="Unauthorized")
    return wrapped

# basic
@router.get("/")
async def index(request):
    return Response(b"Hello Router")

# baca body
@router.post("/echo")
async def echo(request: Request):
    body = await request.body()
    return Response(body)

# get path param
@router.get("/users/{id}")
async def get_users(id):
    if id != "1":
        raise NotFound("user not found")

    return Response(b"user 1")

# get query param /search?q=1&page=2
@router.get("/search")
async def search(q, page="1"):
    msg = f"q={q}, page={page}"
    return Response(msg.encode())

# depends
@router.get("/me")
async def me(profile=Depends(get_profile)):
    return Response(profile.encode())

# background task run
@router.post("/register")
async def register():
    return Response(
        b"registered",
        background=BackgroundTask(send_email, to="test@mail.com")
    )

# simple validasi payload
@router.post("/users")
async def create_user(payload: UserIn):
    return Response(
        f"{payload.name}:{payload.age}".encode()
    )
