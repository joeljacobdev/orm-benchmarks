import asyncio
import os
import time
from random import choice
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from models import Journal, async_session

LEVEL_CHOICE = [10, 20, 30, 40, 50]
concurrents = int(os.environ.get("CONCURRENTS", "10"))


async def _runtest(mi, ma) -> int:
    async with async_session() as session:
        objs = await session.execute(select(Journal).where(Journal.id >= mi).where(Journal.id < ma))
        objs = objs.scalars().all()
        data = [{'id': o.id, 'level': choice(LEVEL_CHOICE), 'text': f"{o.text} Update"} for o in objs]
        insert_statement = insert(Journal).values(data)
        await session.execute(
            insert_statement.on_conflict_do_update(
                constraint=Journal.__table__.primary_key,
                set_=dict(level=insert_statement.excluded.level, text=insert_statement.excluded.text)
            )
        )
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
    print(f"SQLAlchemy ORM{loopstr}, J: Rows/sec: {count / (now - start): 10.2f}")
