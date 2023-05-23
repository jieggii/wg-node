import asyncio

from fastapi import FastAPI

from wg_node.config import config
from wg_node.database import init_database
from wg_node.http.routers import node, peer

# initialize database
loop = asyncio.get_running_loop()
db_init_task = loop.create_task(
    init_database(
        host=config.Mongo.HOST,
        port=config.Mongo.PORT,
        user=config.Mongo.USER,
        password=config.Mongo.PASSWORD,
        database=config.Mongo.DATABASE,
    )
)
db_init_task.add_done_callback(lambda t: print(f"task was finished {t.result()}"))

# initialize FastAPI app
app = FastAPI()
app.include_router(node.router)
app.include_router(peer.router)
