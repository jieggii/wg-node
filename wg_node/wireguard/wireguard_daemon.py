from wg_node.util import execute


def sync_with_config():
    execute("wg syncconf wg0 <(wg-quick strip wg0)")


def init_wireguard_daemon():
    # execute("wg-quick down wg0")
    execute("wg-quick up wg0")
    sync_with_config()

