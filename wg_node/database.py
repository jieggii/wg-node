from datetime import datetime

from beanie import Document, Indexed, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field, root_validator

from wg_node.wireguard.key import generate_keypair, generate_preshared_key

WIREGUARD_PEER_ID_REGEX = r".+"


class WireguardPeer(Document):
    """Represents WireGuard peer."""

    peer_id: Indexed(str, unique=True) = Field(type=str, regex=WIREGUARD_PEER_ID_REGEX)
    address: Indexed(str, unique=True)

    private_key: str
    public_key: str

    preshared_key: str = Field(default_factory=generate_preshared_key)

    created_at: datetime = Field(default_factory=datetime.now)
    enabled: bool = True

    class Settings:
        name = "wireguard-peers"

    @root_validator(pre=True)
    def generate_peer_keypair(cls, values):  # noqa
        # This root validator is required to generate peer's
        # private and public keys if they were not provided.
        if not values.get("private_key") and not values.get("public_key"):
            values["private_key"], values["public_key"] = generate_keypair()
        return values

    def __str__(self) -> str:
        return f"WireguardPeer(peer_id={self.peer_id}, address={self.address})"


class APIUser(Document):
    """Represents an identified trusted API user."""

    public_key: Indexed(str, unique=True)

    is_root_user: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "api-users"

    def __str__(self) -> str:
        return f"APIUser(public_key={self.public_key})"


async def init_database(host: str, port: int, user: str, password: str, database: str):
    """Establishes connection to a database and initializes it."""
    client = AsyncIOMotorClient(f"mongodb://{user}:{password}@{host}:{port}")
    await init_beanie(database=client[database], document_models=[APIUser, WireguardPeer])
