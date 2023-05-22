from datetime import datetime

from beanie import Document
from pydantic import Field, root_validator

from wg_node.wireguard.key import generate_keypair, generate_preshared_key


class Peer(Document):
    uuid: str
    address: str

    private_key: str
    public_key: str

    preshared_key: str = Field(default_factory=generate_preshared_key)

    created_at: datetime = Field(default_factory=datetime.now)
    enabled: bool = True

    class Settings:
        name = "peers"

    @root_validator(pre=True)
    def generate_peer_keypair(cls, values):  # noqa
        """This root validator is required to generate peer's private and public keys"""
        values["private_key"], values["public_key"] = generate_keypair()
        return values

    def __str__(self):
        return f"Peer<uuid={self.uuid}>"
