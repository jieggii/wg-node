from fastapi import APIRouter

router = APIRouter(prefix="")


@router.get("/stats", summary="returns node statistics")
async def stats():
    pass
