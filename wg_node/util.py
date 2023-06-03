import subprocess
from typing import NoReturn

from loguru import logger


def execute(command: str) -> str | NoReturn:
    """
    Executes command in the shell and returns result stdout if it was successful.
    Otherwise, logs an error and raises subprocess.CalledProcessError exception.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, timeout=5, capture_output=True, text=True)
        return result.stdout

    except subprocess.CalledProcessError as err:
        logger.error(f"error running command `{command}`. stdout: `{err.stdout}`; stderr: `{err.stderr}`")
        raise
