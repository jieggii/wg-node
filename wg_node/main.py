import asyncio

from fastapi import FastAPI

from wg_node.http.routers import node, peer
from wg_node.init import init_app

# perform necessary initialization operations
loop = asyncio.get_running_loop()
init_task = loop.create_task(init_app())

# initialize FastAPI app
app = FastAPI()
app.include_router(node.router)
app.include_router(peer.router)
