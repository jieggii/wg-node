from base64 import b64encode

from nacl.public import PrivateKey
from app.models import Peer
from app.config import config


def _key_to_str(key: PrivateKey) -> str:
    return b64encode(bytes(key)).decode("ascii")


def generate_keys() -> (str, str):
    """Generates private and public keys"""
    private_key = PrivateKey.generate()
    return _key_to_str(private_key), _key_to_str(private_key.public_key)


def generate_psk() -> str:
    """Generates preshared key"""
    private_key = PrivateKey.generate()
    return _key_to_str(private_key)

#
#
# def find_free_address(peers: list[Peer]) -> str | None:
#     for i in range(2, 255):
#         address = config.WG.BASE_ADDRESS.replace("x", str(i))
#         for peer in peers:
#             if peer.address == address:
#                 continue
#