import asyncio
import os
import time
from sqlalchemy import delete, select
from models import Journal, async_session

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(mi, ma) -> int:
    async with async_session.begin() as session:
        objs = await session.execute(select(Journal).where(Journal.id >= mi).where(Journal.id < ma))
        objs = objs.scalars().all()
        # ids = []
        for obj in objs:
            # ids.append(obj.id)
            await session.delete(obj)
        # await session.execute(delete(Journal).where(Journal.id.in_(ids)))
        # await session.commit()
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
            *[_runtest(i * inrange, ((i + 1) * inrange) - 1) for i in range(concurrents)]
        )
    )
    now = time.time()
    print(f"SQLAlchemy ORM{loopstr}, L: Rows/sec: {count / (now - start): 10.2f}")
