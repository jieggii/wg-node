import subprocess
# This module simply uses `wg` binary instead of generating keys manually.
# There are couple reasons for that:
# a) I've spent 2 hours to make `pynacl` or `cryptography` packages work in alpine
#    docker container and could not succeed in it.
# b) Even if there is a proper way (it has to be, but it will take some time to find it)
#    to make them work, it will require installation of additional packages, and possibly
#    additional configurations, what will increase build time and image size.


_WG_BINARY = "/usr/bin/wg"


def _exec(command: str) -> str:
    result = subprocess.run(
        command, shell=True, check=True, timeout=5, capture_output=True, text=True
    )
    return result.stdout


def _remove_newline_end(key: str):
    return key.replace("\n", "")


def generate_keypair() -> (str, str):
    """Generates keypair (private and matching public key)"""
    private_key = _remove_newline_end(_exec(f"{_WG_BINARY} genkey"))
    public_key = _remove_newline_end(_exec(f"echo {private_key} | {_WG_BINARY} pubkey"))

    return private_key, public_key


def generate_preshared_key() -> str:
    """Generates preshared key"""
    return _remove_newline_end(_exec(f"{_WG_BINARY} genkey"))
