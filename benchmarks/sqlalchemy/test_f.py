import asyncio
import os
import time
from random import randint
from sqlalchemy import select
from models import Journal, async_session

concurrents = int(os.environ.get("CONCURRENTS", "10"))
count = int(os.environ.get("ITERATIONS", "1000"))
maxval = count - 1
count *= 2


async def _runtest(count):
    for _ in range(count):
        async with async_session() as session:
            result = await session.execute(select(Journal).where(Journal.id == randint(1, maxval)))
            result = result.scalar()


async def runtest(loopstr):
    start = time.time()
    await asyncio.gather(*[_runtest(count // concurrents) for _ in range(concurrents)])
    now = time.time()
    print(f"SQLAlchemy ORM{loopstr}, F: Rows/sec: {count / (now - start): 10.2f}")
