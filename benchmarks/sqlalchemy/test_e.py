import os
import time
import asyncio
from random import randrange
from sqlalchemy import select

from models import Journal, async_session

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get("ITERATIONS", "1000"))
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(_iters) -> int:
    count = 0
    for _ in range(_iters):
        for level in LEVEL_CHOICE:
            async with async_session() as session:
                res = await session.execute(
                    select(Journal).where(Journal.level == level).limit(20).offset(randrange(iters - 20))
                )
                count += len(res.scalars().all())
    return count


async def runtest(loopstr):
    start = time.time()
    count = sum(
        await asyncio.gather(*[_runtest(iters // 10 // concurrents) for _ in range(concurrents)])
    )
    now = time.time()
    print(f"SQLAlchemy ORM{loopstr}, E: Rows/sec: {count / (now - start): 10.2f}")
