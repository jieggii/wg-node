from fastapi import APIRouter
from pydantic import BaseModel

from wg_node.database import WireguardPeer

router = APIRouter(prefix="/node")


class NodeStatusResponse(BaseModel):
    peers_count: int
    enabled_peers_count: int


@router.get("/status", summary="returns peers count and active peers count")
async def node_status() -> NodeStatusResponse:
    peers_count = await WireguardPeer.all().count()
    enabled_peers_count = await WireguardPeer.find(WireguardPeer.enabled == True).count()  # noqa

    return NodeStatusResponse(
        peers_count=peers_count,
        enabled_peers_count=enabled_peers_count,
    )


class NodeWipeResponse(BaseModel):
    peers_deleted: int


@router.delete("/wipe", summary="permanently deletes all peers")
async def node_wipe() -> NodeWipeResponse:
    all_peers = WireguardPeer.all()
    peers_count = await all_peers.count()
    await all_peers.delete()
    return NodeWipeResponse(peers_deleted=peers_count)
