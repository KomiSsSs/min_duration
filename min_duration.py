import asyncio
from time import perf_counter
from typing import Any, Awaitable, Callable, Optional, TypeVar, Coroutine

T = TypeVar("T")


async def run_paced(awaitable: Awaitable[T], min_ms: int = 500) -> T:
  
    start = perf_counter()
    try:
        return await awaitable
    finally:
        elapsed = perf_counter() - start
        remain = (min_ms / 1000.0) - elapsed
        if remain > 0:
            await asyncio.sleep(remain)


def min_exec_time(
    min_ms: int = 500,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Coroutine[Any, Any, T]]]:
    def _decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        async def _wrapped(*args: Any, **kwargs: Any) -> T:
            start = perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed = perf_counter() - start
                remain = (min_ms / 1000.0) - elapsed
                if remain > 0:
                    await asyncio.sleep(remain)

        return _wrapped

    return _decorator


class MinDuration:

    def __init__(self, min_ms: int = 500) -> None:
        self.min_ms = min_ms
        self._start: Optional[float] = None

    async def __aenter__(self) -> "MinDuration":
        self._start = perf_counter()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        start = self._start or perf_counter()
        elapsed = perf_counter() - start
        remain = (self.min_ms / 1000.0) - elapsed
        if remain > 0:
            await asyncio.sleep(remain)
