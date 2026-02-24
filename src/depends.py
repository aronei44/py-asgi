import inspect

from src.request import Request


class Depends:
    def __init__(self, dependency):
        self.dependency = dependency

async def resolve_dependency(dep_fn, request):
    cache = request.state.__dict__.setdefault("_dep_cache", {})

    if dep_fn in cache:
        return cache[dep_fn]

    sig = inspect.signature(dep_fn)
    values = {}

    for name, param in sig.parameters.items():

        if param.annotation is Request:
            values[name] = request
            continue

        if isinstance(param.default, Depends):
            sub_dep = param.default.dependency
            values[name] = await resolve_dependency(sub_dep, request)

    result = dep_fn(**values)
    if inspect.isawaitable(result):
        result = await result

    cache[dep_fn] = result
    return result