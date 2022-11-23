import os
import time
import asyncio
from sqlalchemy import select

from models import Journal, async_session

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(inrange) -> int:
    count = 0
    async with async_session() as session:
        for _ in range(inrange):
            for level in LEVEL_CHOICE:
                res = await session.execute(select(Journal.__table__.columns).where(Journal.level == level))
                res = res.all()
                count += len(res)
    return count


async def runtest(loopstr):
    inrange = 10 // concurrents
    if inrange < 1:
        inrange = 1
    start = time.time()
    count = sum(await asyncio.gather(*[_runtest(inrange) for _ in range(concurrents)]))
    now = time.time()
    print(f"SQLAlchemy ORM{loopstr}, H: Rows/sec: {count / (now - start): 10.2f}")
