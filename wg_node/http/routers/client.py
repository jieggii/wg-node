import asyncio
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel

from wg_node.database import Client
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG, generate_client_address

router = APIRouter(prefix="/client")

loop = asyncio.get_running_loop()


async def update_wg_config() -> None:
    peers = await Client.all().to_list()
    content = WIREGUARD_CONFIG.generate_config_content(peers)
    await WIREGUARD_CONFIG.write(content)
    WIREGUARD_CONFIG.sync()
    logger.info("regenerated and synced Wireguard config")


class ClientCreateResponse(BaseModel):
    address: str


class ClientCreateParams(BaseModel):
    client_id: str


@router.post("/create", summary="creates new peer")
async def client_create(params: ClientCreateParams) -> ClientCreateResponse:
    if await Client.find(Client.client_id == params.client_id).exists():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="client with this client_id already exists"
        )

    taken_addresses = [client.address for client in await Client.all().to_list()]
    address = generate_client_address(taken_addresses)
    if not address:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="no free client addresses left"
        )

    client = Client(client_id=params.client_id, address=address)
    await client.insert()
    await update_wg_config()

    return ClientCreateResponse(address=client.address)


@router.get("/{client_id}/config", summary="returns client's wireguard config")
async def client_get_config(client_id: str) -> PlainTextResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")

    config = WIREGUARD_CONFIG.generate_peer_config(client_id)
    return PlainTextResponse(config)


class ClientUpdateResponse(BaseModel):
    enabled: bool


@router.put("/{client_id}", summary="enables or disables client")
async def client_update(client_id: str, enabled: bool) -> ClientUpdateResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")

    await client_id.set({Client.enabled: enabled})  # noqa
    await update_wg_config()

    return ClientUpdateResponse(enabled=client.enabled)


class ClientDeleteResponse(BaseModel):
    client_id: str


@router.delete("/{client_id}", summary="permanently deletes peer")
async def peer_delete(client_id: str) -> ClientDeleteResponse:
    client = await Client.find_one(Client.client_id == client_id)
    if client is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "client not found")
    await client.delete()
    await update_wg_config()
    return ClientDeleteResponse(client_id=client.client_id)
