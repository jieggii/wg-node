from datetime import datetime

import pymongo
from beanie import Document, Indexed
from pydantic import Field, root_validator

from wg_node.wireguard.key import generate_keypair, generate_preshared_key


class Peer(Document):
    uuid: Indexed(str, index_type=pymongo.TEXT, unique=True)
    # address: Indexed(str, index_type=pymongo.TEXT, unique=True)
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

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Peer<uuid={self.uuid}>"
