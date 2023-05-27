from wg_node.util import execute, remove_newline_end

# This module simply uses `wg` binary instead of generating keys manually.
# There are couple reasons for that:
# a) I've spent 2 hours to make `pynacl` or `cryptography` packages work in alpine
#    docker container and could not succeed in it.
# b) Even if there is a proper way (it has to be, but it will take some time to find it)
#    to make them work, it will require installation of additional packages, and possibly
#    additional configurations, what will increase build time and image size.


def generate_keypair() -> (str, str):
    """Generates keypair (private and matching public key)"""
    private_key = remove_newline_end(execute(f"wg genkey"))
    public_key = remove_newline_end(execute(f"echo {private_key} | wg pubkey"))

    return private_key, public_key


def generate_preshared_key() -> str:
    """Generates preshared key"""
    return remove_newline_end(execute(f"wg genkey"))
