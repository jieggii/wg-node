import datetime

from beanie import Document


class Peer(Document):
    uuid: str
    address: str

    private_key: str
    public_key: str
    preshared_key: str

    created_at: datetime.datetime
    enabled: bool

    class Settings:
        name = "peers"

    def __str__(self):
        return f"Peer<{self.uuid}>"
