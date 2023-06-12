import asyncio
import re
from http import HTTPStatus
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel

from wg_node.database import Client, CLIENT_ID_REGEX
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG, generate_client_address

router = APIRouter(prefix="/client")

loop = asyncio.get_running_loop()


async def update_wg_config() -> None:
    clients = await Client.all().to_list()
    content = WIREGUARD_CONFIG.generate_config_content(clients)
    await WIREGUARD_CONFIG.write(content)
    WIREGUARD_CONFIG.sync()
    logger.info("regenerated and synced Wireguard config")


class ClientCreateResponse(BaseModel):
    address: str


class ClientCreateParams(BaseModel):
    client_id: str


@router.post("/", summary="creates new client")
async def client_create(params: ClientCreateParams) -> ClientCreateResponse:
    if not re.fullmatch(CLIENT_ID_REGEX, params.client_id):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="invalid client identifier")
    if await Client.find(Client.client_id == params.client_id).exists():
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="client with this client_id already exists")

    taken_addresses = [client.address for client in await Client.all().to_list()]
    address = generate_client_address(taken_addresses)
    if not address:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="no free client addresses left")

    client = Client(client_id=params.client_id, address=address)
    await client.insert()
    await update_wg_config()

    return ClientCreateResponse(address=client.address)


class ClientGetResponse(BaseModel):
    client_id: str
    address: str
    enabled: bool
    created_at: datetime


@router.get("/{client_id}", summary="returns information about client")
async def client_get(client_id: str) -> ClientGetResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")
    return ClientGetResponse(
        client_id=client.client_id,
        address=client.address,
        created_at=client.created_at,
        enabled=client.enabled,
    )


class ClientUpdateResponse(BaseModel):
    enabled: bool


@router.put("/{client_id}", summary="enables or disables client")
async def client_update(client_id: str, enabled: bool) -> ClientUpdateResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")

    await client.set({Client.enabled: enabled})  # noqa
    await update_wg_config()

    return ClientUpdateResponse(enabled=client.enabled)


class ClientDeleteResponse(BaseModel):
    client_id: str


@router.delete("/{client_id}", summary="permanently deletes client")
async def client_delete(client_id: str) -> ClientDeleteResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")
    await client.delete()
    await update_wg_config()
    return ClientDeleteResponse(client_id=client.client_id)


@router.get("/{client_id}/config", summary="returns client's wireguard config")
async def client_get_config(client_id: str) -> PlainTextResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")

    config = WIREGUARD_CONFIG.generate_client_config(client)
    return PlainTextResponse(config)
