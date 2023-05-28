from wg_node.config import config
from wg_node.database import Peer
from wg_node.database.init import init_database
from wg_node.docker_secrets import read_docker_secret
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG
from wg_node.wireguard.wireguard_daemon import init_wireguard_daemon


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

    # generate and write Wireguard config file
    peers = await Peer.all().to_list()
    await WIREGUARD_CONFIG.update(peers)

    # initialize Wireguard
    init_wireguard_daemon()
