import subprocess
from typing import NoReturn

from loguru import logger


def pem_rsa_key_to_str(pem_content: str) -> str:  # todo: proper name
    """Extracts public key from string in PEM format."""
    lines = [line for line in pem_content.split("\n") if line]  # skipping empty lines
    if lines[0] != "-----BEGIN RSA PUBLIC KEY-----" or lines[-1] != "-----END RSA PUBLIC KEY-----":
        raise ValueError("invalid PEM content")  # todo
    return "".join(lines[1:-1])


def execute_cmd(command: str) -> str | NoReturn:
    """
    Executes command in the shell and returns result stdout if it was successful.
    Otherwise, stderr and stdout are logged and subprocess.CalledProcessError is raised.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            timeout=5,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"error running command '{command}'. stderr: {e.stderr}; stdout: {e.stdout}")
        raise

    return result.stdout
