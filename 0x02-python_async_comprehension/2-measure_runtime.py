#!/usr/bin/env python3
"""
measure_runtime coroutine that will execute async_comprehension
four times in parallel using asyncio.gather.
"""
import time
import asyncio


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Function to calculate time
    """
    start = time.time()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    end = time.time()
    time_taken = end - start
    return time_taken
