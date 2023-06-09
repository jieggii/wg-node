import asyncio

from fastapi import Depends, FastAPI

from wg_node.http.dependencies import authenticate_client
from wg_node.http.routers import node, client
from wg_node.init import init_app

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
    dependencies=[Depends(authenticate_client)],
)
app.include_router(node.router, tags=["node"])
app.include_router(client.router, tags=["client"])
