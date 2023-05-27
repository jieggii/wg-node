from beanie import init_beanie as _init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from wg_node.database.peer import Peer


async def init_database(host: str, port: int, user: str, password: str, database: str):
    client = AsyncIOMotorClient(f"mongodb://{user}:{password}@{host}:{port}")
    await _init_beanie(database=client[database], document_models=[Peer])
