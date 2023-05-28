import os

from typing import NoReturn


_SECRETS_DIR = "/run/secrets"


def read_docker_secret(filename: str) -> str | NoReturn:
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
