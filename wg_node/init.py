from loguru import logger

from wg_node.config import config
from wg_node.database import Client, init_database
from wg_node.docker_secrets import read_secret_file
from wg_node.util import execute
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG


async def init_app() -> None:
    """
    init_app performs necessary initializations
    (initializes database, creates Wireguard config file and brings up the Wireguard interface)
    """
    # initialize database
    await init_database(
        host=config.Mongo.HOST,
        port=config.Mongo.PORT,
        user=read_secret_file(config.Mongo.USERNAME_FILE),
        password=read_secret_file(config.Mongo.PASSWORD_FILE),
        database=config.Mongo.DATABASE,
    )

    # generate, write and sync Wireguard config
    clients = await Client.all().to_list()
    content = WIREGUARD_CONFIG.generate_config_content(clients)
    await WIREGUARD_CONFIG.write(content)
    execute("wg-quick up wg0")
    WIREGUARD_CONFIG.sync()

    enabled_clients_count = await Client.find(Client.enabled == True).count()  # noqa
    clients_count = await Client.all().count()
    logger.info(
        f"successfully started wg-node. Clients count: {clients_count} ({enabled_clients_count} enabled)",
    )
