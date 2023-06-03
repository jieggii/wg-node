import asyncio
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel

from wg_node.database import Peer
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG, generate_peer_address

router = APIRouter(prefix="/peer")

loop = asyncio.get_running_loop()


async def update_wg_config() -> None:
    peers = await Peer.all().to_list()
    content = WIREGUARD_CONFIG.generate_config_content(peers)
    await WIREGUARD_CONFIG.write(content)
    WIREGUARD_CONFIG.sync()
    logger.info("regenerated and synced Wireguard config")


class CreateResponse(BaseModel):
    address: str


class CreateParams(BaseModel):
    uuid: str


@router.post("/create", summary="creates new peer")
async def create_peer(body: CreateParams) -> CreateResponse:
    addresses = []
    peers = await Peer.all().to_list()
    for _peer in peers:
        if _peer.uuid == body.uuid:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="peer with this uuid already exists")
        addresses.append(_peer.address)

    address = generate_peer_address(taken_addresses=addresses)
    if not address:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="no free addresses left")

    peer = Peer(uuid=body.uuid, address=address)
    await peer.insert()
    await update_wg_config()

    return CreateResponse(address=peer.address)


@router.get("/{uuid}/config", summary="returns peer wireguard config")
async def peer_config(uuid: str) -> PlainTextResponse:
    peer = await Peer.find_one(Peer.uuid == uuid)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")

    config = WIREGUARD_CONFIG.generate_peer_config(peer)
    return PlainTextResponse(config)


class PeerUpdateResponse(BaseModel):
    enabled: bool


@router.put("/{uuid}", summary="enables or disables peer")
async def peer_update(uuid: str, enabled: bool) -> PeerUpdateResponse:
    peer = await Peer.find_one(Peer.uuid == uuid)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")

    await peer.set({Peer.enabled: enabled})  # noqa
    await update_wg_config()

    return PeerUpdateResponse(enabled=peer.enabled)


class PeerDeleteResponse(BaseModel):
    uuid: str


@router.delete("/{uuid}", summary="permanently deletes peer")
async def peer_delete(uuid: str) -> PeerDeleteResponse:
    peer = await Peer.find_one(Peer.uuid == uuid)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")
    await peer.delete()
    await update_wg_config()
    return PeerDeleteResponse(uuid=peer.uuid)
