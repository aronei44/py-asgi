class HTTPException(Exception):
    def __init__(self, status: int, detail: str):
        self.status = status
        self.detail = detail


class BadRequest(HTTPException):
    def __init__(self, detail="Bad Request"):
        super().__init__(400, detail)


class Unauthorized(HTTPException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(401, detail)


class NotFound(HTTPException):
    def __init__(self, detail="Not Found"):
        super().__init__(404, detail)

class ValidationError(HTTPException):
    def __init__(self, detail="Unprocessable Entity"):
        super().__init__(422, detail)