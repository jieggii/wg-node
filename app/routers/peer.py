from fastapi import APIRouter


router = APIRouter(prefix="/peer")


@router.post("/create", summary="creates new peer")
async def create_peer(uuid: str):
    pass


@router.get("/peer/{uuid}/config", summary="returns peer wireguard config")
async def peer_config(uuid: str):
    pass


@router.get("/peer/{uuid}/stats", summary="returns peer statistics")
async def peer_stats(uuid: str):
    pass


@router.put("/peer/{uuid}", summary="enables or disables peer")
async def peer_update(enabled: bool):
    pass


@router.delete("/peer/{uuid}", summary="permanently deletes peer")
async def peer_delete(uuid: str):
    pass
