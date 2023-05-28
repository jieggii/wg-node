import subprocess
from loguru import logger


def remove_newline_end(key: str):
    return key.replace("\n", "")


def execute(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, check=True, timeout=5, capture_output=True, text=True
        )
        logger.info(f"exec ${command} -> {result.stdout}")
        return result.stdout

    except subprocess.CalledProcessError as err:
        logger.error(f"exec ${command} -> {err.stdout}; STDERR: {err.stderr}")
