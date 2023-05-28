import pathlib

from aiofile import async_open
from loguru import logger

from wg_node.config import config
from wg_node.database import Peer
from wg_node.wireguard.key_storage import KeyStorage

# These constants are defined here and not in any other place (e.g. not in ENV variables)
# mostly because they are not meant to be changed and also to prevent confusion
_SERVER_INTERFACE_ADDRESS = "10.0.0.1/16"
_SERVER_INTERFACE_LISTEN_PORT = 51820
_SERVER_INTERFACE_DEVICE = "eth0"

_PEER_INTERFACE_ADDRESS_PATTERN = "10.0.x.y/16"
_PEER_PERSISTENT_KEEPALIVE = 0
_PEER_DNS = "1.1.1.1, 8.8.8.8"


def generate_peer_address(taken_addresses: list[str]) -> str | None:
    """Generates free IP address for a new peer"""

    # adding server address to list of taken addresses 'cause it cannot be used for new peer
    taken_addresses.append(_SERVER_INTERFACE_ADDRESS)
    for x in range(1, 255):
        for y in range(1, 255):
            address = _PEER_INTERFACE_ADDRESS_PATTERN.replace("x", str(x)).replace("y", str(y))
            if address not in taken_addresses:
                return address
    return None


class WireguardConfig:
    """
    WireguardConfig is interface to interact with Wireguard configuration files
    It has methods to generate its content and to write it to the file
    """

    _path: pathlib.PosixPath

    _private_key: str
    _public_key: str

    def __init__(self, path: str, *, private_key: str, public_key: str):
        self._path = pathlib.PosixPath(path)
        self._private_key = private_key
        self._public_key = public_key

    async def _write(self, content: str):
        async with async_open(self._path, "w") as file:
            await file.write(content)

    async def _generate_config(self, peers: list[Peer]) -> str:
        """
        Generates and returns wireguard config content according to peers and server settings.
        """
        content = f"""# generated by wg-node
 
[Interface]
PrivateKey = {self._private_key}
Address = {_SERVER_INTERFACE_ADDRESS}
ListenPort = {_SERVER_INTERFACE_LISTEN_PORT}
"""
        for i, peer in enumerate(peers):
            if peer.enabled:
                content += f"""
# uuid={peer.uuid}
[Peer]
PublicKey = {peer.public_key}
PresharedKey = {peer.preshared_key}
AllowedIPs = {peer.address}
"""
        print(content, flush=True)
        return content

    def generate_peer_config(self, peer: Peer) -> str:
        """Generates and returns config for an individual peer"""
        content = f"""[Interface]
PrivateKey = {peer.private_key}
Address = {peer.address}
DNS = {_PEER_DNS}

[Peer]
PublicKey = {self._public_key}
PresharedKey = {peer.preshared_key}
Endpoint = {config.Wireguard.HOSTNAME}:{config.Wireguard.PORT}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = {_PEER_PERSISTENT_KEEPALIVE}
"""

        return content

    async def update(self, peers: list[Peer]) -> None:
        """
        Generates config content and writes it to the config file
        """
        content = await self._generate_config(peers)
        await self._write(content)


# initialize server key storage
_key_storage = KeyStorage(
    "/etc/wg-node/server-keys.json"  # remember to update mount point in docker-compose.yml when updating this path
)
if not _key_storage.exists():
    _key_storage.generate_and_store_keys()
    logger.info("generated and stored public keys for the server")

# initialize wireguard config
_private_key, _public_key = _key_storage.read_keys()

WIREGUARD_CONFIG = WireguardConfig(
    "/etc/wireguard/wg0.conf", private_key=_private_key, public_key=_public_key
)
