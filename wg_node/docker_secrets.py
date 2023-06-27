import os
from typing import NoReturn

_SECRETS_DIR = "/run/secrets"
_NODE_ADMIN_PUBLIC_KEYS_DIR = os.path.join(_SECRETS_DIR, "node_clients_public_keys")


def _extract_public_key_from_pem(content: str) -> str:
    """Extracts public key from string in PEM format."""
    lines = [line for line in content.split("\n") if line]  # skipping empty lines
    if lines[0] != "-----BEGIN RSA PUBLIC KEY-----" or lines[-1] != "-----END RSA PUBLIC KEY-----":
        raise ValueError("invalid PEM content")
    return "".join(lines[1:-1])


def read_secret_file(filename: str) -> str | NoReturn:
    """Reads and returns docker secret file content."""
    filepath = os.path.join(_SECRETS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            raise ValueError(f"docker secret file {filepath} is empty")
        return content


def read_node_clients_public_keys() -> list[str]:
    """
    Reads and returns list of node clients' public keys
    (from the node_client_public_keys docker secret).
    """
    public_keys: list[str] = []
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
        raise ValueError("no node clients' keys were specified")

    return public_keys
