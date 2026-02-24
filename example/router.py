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

@router.middleware
async def auth(handler):
    print("🔥 DIPANGGIL")
    async def wrapped(req):
        raise HTTPException(status=401,detail="Unauthorized")
        # if req.headers.get("x-token") != "secret":
        # return await handler(req)
    return wrapped

@router.get("/")
async def index(request):
    return Response(b"Hello Router")

@router.post("/echo")
async def echo(request: Request):
    body = await request.body()
    return Response(body)

@router.get("/users/{id}")
async def get_users(id):
    if id != "1":
        raise NotFound("user not found")

    return Response(b"user 1")

@router.get("/search")
async def search(q, page="1"):
    msg = f"q={q}, page={page}"
    return Response(msg.encode())

@router.get("/state-test")
async def state_test():
    # request belum diinject ke handler param
    # kita baca langsung dari middleware effect via closure
    return Response(b"OK")

@router.get("/me")
async def me(profile=Depends(get_profile)):
    return Response(profile.encode())

@router.post("/register")
async def register():
    return Response(
        b"registered",
        background=BackgroundTask(send_email, to="test@mail.com")
    )

@router.post("/users")
async def create_user(payload: UserIn):
    return Response(
        f"{payload.name}:{payload.age}".encode()
    )
