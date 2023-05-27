import subprocess


def remove_newline_end(key: str):
    return key.replace("\n", "")


def execute(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, check=True, timeout=5, capture_output=True, text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as err:
        from loguru import logger
        logger.error(f"{err.stderr} {err.stdout}")

