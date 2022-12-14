#!/usr/bin/env python
import os
import sys
import logging

try:
    concurrents = int(os.environ.get("CONCURRENTS", "10"))

    if concurrents != 10:
        loopstr = f" C{concurrents}"
    else:
        loopstr = ""
    if os.environ.get("UVLOOP", ""):
        import asyncio

        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
finally:
    pass

if concurrents > 1 and sys.version_info < (3, 7):
    sys.exit()

db_url = f"postgres://joel:joeljacob@0.0.0.0:9500/tbench"

import test_a
import test_b
import test_c
import test_d
import test_e
import test_f
import test_g
import test_h
import test_i
import test_j
import test_k
import test_l
from tortoise import Tortoise, run_async


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(db_url=db_url, modules={"models": ["models"]})


async def create_db():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()


async def run_benchmarks():
    await create_db()
    await test_a.runtest(loopstr)
    await test_b.runtest(loopstr)
    await test_c.runtest(loopstr)
    await test_d.runtest(loopstr)
    await test_e.runtest(loopstr)
    await test_f.runtest(loopstr)
    await test_g.runtest(loopstr)
    await test_h.runtest(loopstr)
    await test_i.runtest(loopstr)
    await test_j.runtest(loopstr)
    await test_k.runtest(loopstr)
    await test_l.runtest(loopstr)


# fmt = logging.Formatter(
#     fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# sh = logging.StreamHandler(sys.stdout)
# sh.setLevel(logging.DEBUG)
# sh.setFormatter(fmt)
#
# # will print debug sql
# logger_db_client = logging.getLogger("tortoise.db_client")
# logger_db_client.setLevel(logging.DEBUG)
# logger_db_client.addHandler(sh)

run_async(run_benchmarks())
