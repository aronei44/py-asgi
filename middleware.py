import time

def logger_middleware(next_handler):
    async def handler(request):
        start = time.time()
        response = await next_handler(request)
        duration = (time.time() - start) * 1000

        print(
            f"{request.method} {request.path} "
            f"{response.status} "
            f"{duration:.2f}ms"
        )
        return response
    return handler

def timing_middleware(next_handler):
    async def handler(request):
        start = time.time()
        response = await next_handler(request)
        response.headers.append(
            (b"x-process-time", f"{time.time()-start:.4f}".encode())
        )
        return response
    return handler