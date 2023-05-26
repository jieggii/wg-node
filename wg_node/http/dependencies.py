from fastapi import Header, HTTPException
from typing_extensions import Annotated


async def verify_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != "fake-super-secret-key":
        raise HTTPException(status_code=401, detail="X-API-Key header invalid")
    return x_api_key
