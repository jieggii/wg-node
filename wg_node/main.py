import asyncio
import sys

from fastapi import FastAPI, Depends

from wg_node.http.routers import node, peer
from wg_node.init import init_app
from wg_node.http.dependencies import validate_request_signature

# perform necessary initialization operations
loop = asyncio.get_running_loop()
init_task = loop.create_task(init_app())


def check_init_task_exception(_):
    exception = init_task.exception()
    if exception:
        raise exception


init_task.add_done_callback(check_init_task_exception)


# initialize FastAPI app
app = FastAPI(
    title="wg-node",
    description="Deploy and manage your Wireguard nodes with one hand!",
    dependencies=[Depends(validate_request_signature)]
)
app.include_router(node.router)
app.include_router(peer.router)
