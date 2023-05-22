from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from wg_node.database import Peer
from wg_node.wireguard.key_storage import KeyStorage
from wg_node.wireguard.wireguard_config import WireguardConfig, generate_peer_address

router = APIRouter(prefix="/peer")

# initialize server key storage
key_storage = KeyStorage(
    path="/etc/wireguard-node/server-keys.json"
)  # remember to update mount point in docker-compose.yml when updating path
if not key_storage.exists():
    key_storage.generate_keys_and_store()

# initialize wireguard config
private_key, public_key = key_storage.read_keys()
wireguard_config = WireguardConfig(
    path="/etc/wireguard/wg0.conf", private_key=private_key, public_key=public_key
)


class CreateResponse(BaseModel):
    uuid: str


@router.post("/create", summary="creates new peer")
async def create_peer(uuid: str) -> CreateResponse:
    peers = await Peer.all().to_list()
    address = generate_peer_address(taken_addresses=[peer.address for peer in peers])
    if not address:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="no free addresses left")

    peer = Peer(uuid=uuid, address=address)
    await peer.insert()
    wireguard_config.update(await Peer.all().to_list())

    return CreateResponse(uuid=peer.uuid)


class ConfigResponse(BaseModel):
    config: str


@router.get("/peer/{uuid}/config", summary="returns peer wireguard config")
async def peer_config(uuid: str) -> ConfigResponse:
    peer = await Peer.find_one(Peer.uuid == uuid)
    if peer is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="peer not found")

    config = wireguard_config.get_peer_config(peer)
    return ConfigResponse(config=config)


@router.get("/peer/{uuid}/stats", summary="returns peer statistics")
async def peer_stats(uuid: str):
    pass


@router.put("/peer/{uuid}", summary="enables or disables peer")
async def peer_update(enabled: bool):
    pass


@router.delete("/peer/{uuid}", summary="permanently deletes peer")
async def peer_delete(uuid: str):
    pass
