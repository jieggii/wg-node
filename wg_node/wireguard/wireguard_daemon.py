from wg_node.util import execute


def init_wireguard_daemon():
    output = execute("cat /etc/wireguard/wg0.conf")
    from loguru import logger
    logger.debug(output)
    execute("wg-quick down wg0")
    execute("wg-quick up wg0")


def sync_with_config():
    pass
