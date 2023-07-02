import asyncio
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel, Field

from wg_node.database import WIREGUARD_PEER_ID_REGEX, WireguardPeer
from wg_node.wireguard.wireguard_config import WIREGUARD_CONFIG, generate_peer_address

router = APIRouter(prefix="/peer")

loop = asyncio.get_running_loop()


async def update_wg_config() -> None:
    peers = await WireguardPeer.all().to_list()
    content = WIREGUARD_CONFIG.generate_config_content(peers)
    await WIREGUARD_CONFIG.write(content)
    WIREGUARD_CONFIG.sync()
    logger.info("regenerated and synced WireGuard config")


class PeerCreateResponse(BaseModel):
    address: str


class PeerCreateParams(BaseModel):
    peer_id: str = Field(regex=WIREGUARD_PEER_ID_REGEX)


@router.post("/", summary="creates new peer")
async def peer_create(params: PeerCreateParams) -> PeerCreateResponse:
    if await WireguardPeer.find(WireguardPeer.peer_id == params.peer_id).exists():
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="peer with such peer_id already exists")

    taken_addresses = [peer.address for peer in await WireguardPeer.all().to_list()]
    address = generate_peer_address(taken_addresses)
    if not address:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="no free peer addresses left")

    peer = WireguardPeer(peer_id=params.peer_id, address=address)
    await peer.insert()
    await update_wg_config()

    return PeerCreateResponse(address=peer.address)


class PeerReadResponse(BaseModel):
    peer_id: str
    address: str
    enabled: bool
    created_at: datetime


@router.get("/{peer_id}", summary="returns information about peer")
async def peer_read(peer_id: str) -> PeerReadResponse:
    peer = await WireguardPeer.find_one(WireguardPeer.peer_id == peer_id)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")
    return PeerReadResponse(
        peer_id=peer.peer_id,
        address=peer.address,
        created_at=peer.created_at,
        enabled=peer.enabled,
    )


class PeerUpdateResponse(BaseModel):
    enabled: bool


@router.put("/{peer_id}", summary="enables or disables peer")
async def peer_update(peer_id: str, enabled: bool) -> PeerUpdateResponse:
    peer = await WireguardPeer.find_one(WireguardPeer.peer_id == peer_id)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")

    await peer.set({WireguardPeer.enabled: enabled})  # noqa
    await update_wg_config()

    return PeerUpdateResponse(enabled=peer.enabled)


class PeerDeleteResponse(BaseModel):
    peer_id: str


@router.delete("/{peer_id}", summary="permanently deletes peer")
async def peer_delete(peer_id: str) -> PeerDeleteResponse:
    peer = await WireguardPeer.find_one(WireguardPeer.peer_id == peer_id)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")
    await peer.delete()
    await update_wg_config()
    return PeerDeleteResponse(peer_id=peer.peer_id)


@router.get("/{peer_id}/config", summary="returns peer's wireguard config")
async def peer_read_config(peer_id: str) -> PlainTextResponse:
    peer = await WireguardPeer.find_one(WireguardPeer.peer_id == peer_id)
    if peer is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "peer not found")

    config = WIREGUARD_CONFIG.generate_peer_config(peer)
    return PlainTextResponse(config)
