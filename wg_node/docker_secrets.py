from typing import NoReturn


def read_docker_secret(path: str) -> str | NoReturn:
    """Reads and returns docker secret file content."""
    with open(path, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            raise ValueError(f"docker secret file {path} is empty")
        return content
