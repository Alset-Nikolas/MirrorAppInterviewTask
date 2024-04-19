import asyncio
import functools


def async_partial(func, *args, **kwargs):
    @functools.wraps(func)
    async def wrapper(*a_args, **a_kwargs):
        result = func(*args, *a_args, **kwargs, **a_kwargs)
        if asyncio.iscoroutinefunction(func):
            result = await result
        return result

    return wrapper
