import os
from typing import NoReturn

_SECRETS_DIR = "/run/secrets"
_NODE_ADMIN_PUBLIC_KEYS_DIR = os.path.join(_SECRETS_DIR, "node_clients_public_keys")


def _extract_public_key_from_pem(content: str) -> bytes:
    """Extracts public key from string in PEM format."""
    lines = [line for line in content.split("\n") if line]  # skipping empty lines
    if lines[0] != "-----BEGIN RSA PUBLIC KEY-----" or lines[-1] != "-----END RSA PUBLIC KEY-----":
        raise ValueError("invalid PEM content")
    return "".join(lines[1:-1]).encode()


def read_secret_file(filename: str) -> str | NoReturn:
    """Reads and returns docker secret file."""
    path = os.path.join(_SECRETS_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                # todo: is RuntimeError is suitable exception class for this case?
                raise RuntimeError(f"docker secret file {path} is empty")
            return content

    except FileNotFoundError:
        raise FileNotFoundError(f"docker secret file {path} not found")


def read_node_clients_public_keys() -> list[bytes]:
    """
    Reads and returns list of node client public keys
    (from node_client_public_keys docker secret).
    """
    public_keys: list[bytes] = []
    for filename in os.listdir(_NODE_ADMIN_PUBLIC_KEYS_DIR):
        filepath = os.path.join(_NODE_ADMIN_PUBLIC_KEYS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            pem_content = file.read()
            try:
                key = _extract_public_key_from_pem(pem_content)
            except ValueError:
                raise ValueError(f"invalid PEM content in clients public key file {filepath}")
            public_keys.append(key)

    if not public_keys:
        raise RuntimeError("no node clients keys were specified")  # todo

    return public_keys
