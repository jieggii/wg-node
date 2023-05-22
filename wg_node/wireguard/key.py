from base64 import b64encode

from nacl.public import PrivateKey


def _key_to_str(key: PrivateKey) -> str:
    """Converts PrivateKey to string which is key"""
    return b64encode(bytes(key)).decode("ascii")


def generate_keypair() -> (str, str):
    """Generates private and public keys"""
    private_key = PrivateKey.generate()
    return _key_to_str(private_key), _key_to_str(private_key.public_key)


def generate_preshared_key() -> str:
    """Generates preshared key"""
    private_key = PrivateKey.generate()
    return _key_to_str(private_key)
