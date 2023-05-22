import asyncio

from fastapi import FastAPI

from wg_node.config import config
from wg_node.database import init_database
from wg_node.http.routers import peer, node

# initialize database
asyncio.run(
    init_database(
        host=config.Mongo.HOST,
        port=config.Mongo.PORT,
        user=config.Mongo.USER,
        password=config.Mongo.PASSWORD,
        database=config.Mongo.DATABASE,
    )
)

# initialize FastAPI app
app = FastAPI()
app.include_router(node.router)
app.include_router(peer.router)
