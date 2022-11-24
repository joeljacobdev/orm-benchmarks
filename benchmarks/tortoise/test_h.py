import asyncio
import os
import time

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(inrange) -> int:
    count = 0
    for _ in range(inrange):
        for level in LEVEL_CHOICE:
            res = list(await Journal.filter(level=level).all().values_list())
            count += len(res)
    return count


async def runtest(loopstr):
    inrange = 10 // concurrents
    if inrange < 1:
        inrange = 1
    start = time.time()
    count = sum(await asyncio.gather(*[_runtest(inrange) for _ in range(concurrents)]))
    now = time.time()
    print(f"Tortoise ORM{loopstr}, H: Rows/sec: {count / (now - start): 10.2f}")
