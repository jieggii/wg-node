import asyncio

from fastapi import Depends, FastAPI
from loguru import logger

from wg_node.env import env
from wg_node.database import APIUser, WireguardPeer, init_database
from wg_node.docker_secrets import read_docker_secret
from wg_node.http.dependencies import verify_request_signature
from wg_node.http.routers import api_user, node, peer
from wg_node.util import execute_cmd, pem_rsa_key_to_str
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG


async def init_app() -> None:
    """
    Performs all necessary initializations which are required before starting the application:
    - Initializes database.
    - Creates WireGuard configuration file.
    - Brings up the wg0 WireGuard interface.
    """

    # initialize database:
    await init_database(
        host=env.Mongo.HOST,
        port=env.Mongo.PORT,
        user=read_docker_secret(env.Mongo.USERNAME_FILE),
        password=read_docker_secret(env.Mongo.PASSWORD_FILE),
        database=read_docker_secret(env.Mongo.DATABASE_FILE),
    )

    # create root API user if it doesn't exist:
    root_api_user_public_key = pem_rsa_key_to_str(
        read_docker_secret(env.Node.ROOT_API_USER_PUBLIC_KEY_FILE),
    )
    root_api_user = await APIUser.find_one(APIUser.public_key == root_api_user_public_key)
    if root_api_user is None:
        await APIUser(public_key=root_api_user_public_key, is_root_user=True).insert()
        logger.info(f"created root API user")
    else:
        # ensure that existing root user is marked as root in the database
        assert root_api_user.is_root_user

    # generate, write and sync WireGuard config:
    peers = await WireguardPeer.all().to_list()  # fetch all peers

    content = WIREGUARD_CONFIG.generate_config_content(peers)  # generate text content of the config file
    await WIREGUARD_CONFIG.write(content)  # write content to the config file

    execute_cmd("wg-quick up wg0")  # bring up the WireGuard interface
    WIREGUARD_CONFIG.sync()  # apply saved configuration

    enabled_peers_count = await WireguardPeer.find(WireguardPeer.enabled == True).count()  # noqa


loop = asyncio.get_running_loop()
init_app_task = loop.create_task(init_app())


def init_app_task_done_callback(task: asyncio.Task):
    exception = task.exception()
    if exception:
        raise RuntimeError(f"got exception during wg-node initialization: {exception}")
    logger.info("successfully initialized wg-node application")


init_app_task.add_done_callback(init_app_task_done_callback)

app = FastAPI(
    title="wg-node",
    description="Deploy and manage your WireGuard nodes with one hand!",
    dependencies=[Depends(verify_request_signature)],  # global dependency which verifies signatures of every request
)
app.include_router(api_user.router, tags=["api-user"])
app.include_router(node.router, tags=["node"])
app.include_router(peer.router, tags=["peer"])
