from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field, root_validator

from wg_node.wireguard.key import generate_keypair, generate_preshared_key


class Client(Document):
    client_id: Indexed(str, unique=True)
    address: Indexed(str, unique=True)

    private_key: str
    public_key: str

    preshared_key: str = Field(default_factory=generate_preshared_key)

    created_at: datetime = Field(default_factory=datetime.now)
    enabled: bool = True

    class Settings:
        name = "clients"

    @root_validator(pre=True)
    def generate_peer_keypair(cls, values):  # noqa
        """
        This root validator is required to generate client's private and public keys
        if they were not provided.
        """
        if not values.get("private_key") and not values.get("public_key"):
            values["private_key"], values["public_key"] = generate_keypair()
        return values

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Client<uuid={self.uuid}>"


async def get_all_peers() -> list[Client]:
    return await Client.all().to_list()
