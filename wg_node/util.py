import subprocess
from typing import NoReturn


def pem_rsa_key_to_str(pem_content: str) -> str:  # todo: proper name
    """Extracts public key from string in PEM format."""
    lines = [line for line in pem_content.split("\n") if line]  # skipping empty lines
    if lines[0] != "-----BEGIN RSA PUBLIC KEY-----" or lines[-1] != "-----END RSA PUBLIC KEY-----":
        raise ValueError("invalid PEM content")  # todo
    return "".join(lines[1:-1])


def execute_cmd(command: str) -> str | NoReturn:
    """
    Executes command in the shell and returns result stdout if it was successful.
    Otherwise, subprocess.CalledProcessError is raised.
    """
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        timeout=5,
        capture_output=True,
        text=True,
    )
    return result.stdout
