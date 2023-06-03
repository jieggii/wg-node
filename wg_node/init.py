from wg_node.config import config
from wg_node.database import init_database, get_all_peers
from wg_node.docker_secrets import read_docker_secret
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG
from wg_node.util import execute


async def init_app() -> None:
    """
    init_app performs necessary initializations
    (initializes database, creates Wireguard config file and brings up the Wireguard interface)
    """
    # initialize database
    await init_database(
        host=config.Mongo.HOST,
        port=config.Mongo.PORT,
        user=read_docker_secret(config.Mongo.USERNAME_FILE),
        password=read_docker_secret(config.Mongo.PASSWORD_FILE),
        database=config.Mongo.DATABASE,
    )

    # generate, write and sync Wireguard config
    peers = await get_all_peers()
    content = WIREGUARD_CONFIG.generate_config_content(peers)
    await WIREGUARD_CONFIG.write(content)

    execute("wg-quick up wg0")
    WIREGUARD_CONFIG.sync()
