from src.request import Request


def get_user(request: Request):
    return request.state.user