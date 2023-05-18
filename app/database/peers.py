from app.models import Peer


async def get_all_peers() -> list[Peer]:
    return await Peer.all().to_list()
