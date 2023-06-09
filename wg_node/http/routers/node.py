from fastapi import APIRouter
from pydantic import BaseModel

from wg_node.database import Client

router = APIRouter(prefix="/node")


class NodeStatusResponse(BaseModel):
    clients_count: int
    enabled_clients_count: int


@router.get("/status", summary="returns clients count and active clients count")
async def status() -> NodeStatusResponse:
    clients_count = await Client.all().count()
    enabled_clients_count = await Client.find(Client.enabled == True).count()  # noqa

    return NodeStatusResponse(
        clients_count=clients_count,
        enabled_clients_count=enabled_clients_count,
    )


class NodeWipeResponse(BaseModel):
    clients_deleted: int


@router.delete("/wipe", summary="permanently deletes all clients")
async def wipe() -> NodeWipeResponse:
    # todo
    return NodeWipeResponse(clients_deleted=-999)
