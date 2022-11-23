import os
import time
import asyncio
from sqlalchemy import select
from models import Journal, async_session

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))

count = 0


async def _runtest(_):
    global count
    async with async_session() as session:
        for _ in range(10):
            for level in LEVEL_CHOICE:
                res = await session.execute(select(Journal).where(Journal.level == level))
                count += len(res.scalars().all())


async def runtest(loopstr):
    start = time.time()
    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])
    now = time.time()
    print(f"SQLAlchemy ORM {loopstr}, D: Rows/sec: {count / (now - start): 10.2f}")
