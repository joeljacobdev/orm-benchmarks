import asyncio
import os
import time
from random import choice

from models import Journal
from tortoise.transactions import in_transaction

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(mi, ma) -> int:
    objs = list(await Journal.filter(id__gte=mi, id__lt=ma).all())
    async with in_transaction():
        for obj in objs:
            await obj.delete()
    return len(objs)


async def runtest(loopstr):
    objs = list(await Journal.all())
    inrange = len(objs) // concurrents
    if inrange < 1:
        inrange = 1
    start = time.time()
    count = sum(
        await asyncio.gather(
            *[_runtest(i * inrange, ((i + 1) * inrange) - 1) for i in range(concurrents)]
        )
    )
    now = time.time()
    print(f"Tortoise ORM{loopstr}, L: Rows/sec: {count / (now - start): 10.2f}")
