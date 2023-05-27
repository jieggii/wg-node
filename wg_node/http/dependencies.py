from fastapi import Header, HTTPException
from typing_extensions import Annotated

# from wg_node.config import config
from wg_node.docker_secrets import read_docker_secret


# read node master's public keys from the docker secret file
master_public_keys = read_docker_secret("node_master_public_keys").split("\n")


async def verify_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != "fake-super-secret-key":
        raise HTTPException(status_code=401, detail="X-API-Key header invalid")
    return x_api_key
