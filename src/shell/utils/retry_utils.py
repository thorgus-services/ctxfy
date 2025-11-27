import asyncio
import time
from typing import Awaitable, Callable, TypeVar

T = TypeVar('T')

def execute_with_retry(fn: Callable[[], T], max_retries: int = 3) -> T:
    """Execute function with retry strategy"""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)  # Fixed delay between retries
    # This line should never be reached, but added to satisfy mypy
    raise RuntimeError("Unexpected state in execute_with_retry")


async def execute_async_with_retry(coro: Callable[[], Awaitable[T]], max_retries: int = 3) -> T:
    """Execute async function with retry strategy"""
    for attempt in range(max_retries):
        try:
            return await coro()
        except Exception:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(1)  # Fixed delay between retries
    # This line should never be reached, but added to satisfy mypy
    raise RuntimeError("Unexpected state in execute_async_with_retry")


def execute_with_error_handling(
    fn: Callable[[], T],
    error_handler: Callable[[Exception], T]
) -> T:
    """Execute function with error handling"""
    try:
        return fn()
    except Exception as e:
        return error_handler(e)