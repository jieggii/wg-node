from fastapi import APIRouter
from pydantic import BaseModel

from wg_node.database import Peer

router = APIRouter(prefix="")


class NodeStatusResponse(BaseModel):
    peers_count: int
    enabled_peers_count: int
    disabled_peers_count: int


@router.get("/status", summary="returns node statistics")
async def stats():
    enabled_peers = await Peer.find_all(Peer.enabled == True).count()  # noqa
    disabled_peers = await Peer.find_all(Peer.enabled == False).count()  # noqa
    return NodeStatusResponse(
        peers_count=enabled_peers + disabled_peers, enabled_peers=enabled_peers, disabled_peers=disabled_peers
    )
