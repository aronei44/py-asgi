import json
from .exceptions import HTTPException
from .response import Response

def error_middleware(next_handler):
    async def handler(request):
        try:
            return await next_handler(request)
        except HTTPException as e:
            body = json.dumps({
                "error": e.detail
            }).encode()

            return Response(
                body=body,
                status=e.status,
                headers=[(b"content-type", b"application/json")]
            )
        except Exception as e:
            # unexpected error
            body = json.dumps({
                "error": "Internal Server Error"
            }).encode()

            return Response(
                body=body,
                status=500,
                headers=[(b"content-type", b"application/json")]
            )
    return handler