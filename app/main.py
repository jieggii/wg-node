import asyncio

from fastapi import FastAPI

from app.config import config
from app.database import init_database
from app.wireguard.key_storage import KeyStorage
from app.wireguard.wireguard_config import WireguardConfig

KEY_STORAGE_PATH = "/etc/wireguard-node/server-keys.json"  # remember to change mountpoint in docker-compose.yml / docker command when changing this variable

# initialize database
asyncio.run(
    init_database(
        host=config.Mongo.HOST,
        port=config.Mongo.PORT,
        user=config.Mongo.USER,
        password=config.Mongo.PASSWORD,
        database=config.Mongo.DATABASE,
    )
)

# initialize server key storage
key_storage = KeyStorage(path=KEY_STORAGE_PATH)
if not key_storage.exists():
    key_storage.generate_keys_and_store()

# initialize wireguard config
wireguard_config = WireguardConfig(path="/etc/wireguard/wg0.conf", key_storage=key_storage)

app = FastAPI()

