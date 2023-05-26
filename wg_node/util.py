import subprocess


def execute(command: str) -> str:
    result = subprocess.run(
        command, shell=True, check=True, timeout=5, capture_output=True, text=True
    )
    return result.stdout
