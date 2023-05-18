import datetime

from beanie import init_beanie as _init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.peer import Peer


async def init_database(host: str, port: int, user: str, password: str, database: str):
    # client = AsyncIOMotorClient(f"database://{user}:{password}@{host}:{port}")
    client = AsyncIOMotorClient("database://localhost:27017")
    await _init_beanie(database=client[database], document_models=[Peer])
