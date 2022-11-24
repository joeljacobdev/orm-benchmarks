import os
import time
from random import choice

from models import Journal, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get("ITERATIONS", "1000"))


Session = sessionmaker(bind=engine)
start = now = time.time()
session = Session()
session.bulk_save_objects(
    [Journal(level=choice(LEVEL_CHOICE), text=f"Insert from C, item {i}") for i in range(count)]
)
session.commit()
now = time.time()

print(f"SyncSQLAlchemy ORM, C: Rows/sec: {count / (now - start): 10.2f}")
