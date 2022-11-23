import asyncio
import os
import time
from random import choice
from sqlalchemy import select
from models import Journal, async_session

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(mi, ma) -> int:
    async with async_session() as session:
        objs = await session.execute(select(Journal).where(Journal.id >= mi).where(Journal.id < ma))
        objs = objs.scalars().all()
        for obj in objs:
            obj.level = choice(LEVEL_CHOICE)
            await session.commit()
    return len(objs)


async def runtest(loopstr):
    async with async_session() as session:
        objs = await session.execute(select(Journal))
        objs = objs.scalars().all()
    inrange = len(objs) // concurrents
    if inrange < 1:
        inrange = 1
    start = time.time()
    count = sum(
        await asyncio.gather(
            *[_runtest(i * inrange or 1, ((i + 1) * inrange) - 1) for i in range(concurrents)]
        )
    )
    now = time.time()
    print(f"SQLAlchemy ORM{loopstr}, K: Rows/sec: {count / (now - start): 10.2f}")
