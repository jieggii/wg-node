import subprocess
from typing import NoReturn


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
