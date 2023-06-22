import asyncio

from fastapi import Depends, FastAPI
from loguru import logger

from wg_node.config import config
from wg_node.database import Client, init_database
from wg_node.docker_secrets import read_secret_file
from wg_node.http.dependencies import verify_request
from wg_node.http.routers import client, node
from wg_node.util import execute_cmd
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG


async def init_app() -> None:
    """
    Performs all necessary initializations which are required before starting the application:
    - initializes database
    - creates WireGuard configuration file
    - brings up the wg0 WireGuard interface
    """

    # initialize database
    await init_database(
        host=config.Mongo.HOST,
        port=config.Mongo.PORT,
        user=read_secret_file(config.Mongo.USERNAME_FILE),
        password=read_secret_file(config.Mongo.PASSWORD_FILE),
        database=config.Mongo.DATABASE,
    )

    # generate, write and sync WireGuard config
    clients = await Client.all().to_list()  # fetch all clients
    content = WIREGUARD_CONFIG.generate_config_content(clients)  # generate text content of the config file
    await WIREGUARD_CONFIG.write(content)  # write content to the config file
    execute_cmd("wg-quick up wg0")  # bring up the WireGuard interface
    WIREGUARD_CONFIG.sync()  # apply saved configuration

    enabled_clients_count = await Client.find(Client.enabled == True).count()  # noqa
    clients_count = await Client.all().count()
    logger.info(
        "successfully initialized wg-node application. "
        f"clients count: {clients_count} ({enabled_clients_count} enabled)",
    )


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
    description="Deploy and manage your WireGuard nodes with one hand!",
    dependencies=[Depends(verify_request)],
)
app.include_router(node.router, tags=["node"])
app.include_router(client.router, tags=["client"])
