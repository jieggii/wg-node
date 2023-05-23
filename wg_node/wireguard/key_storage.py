import json
import pathlib

from .key import generate_keypair


class KeyStorage:
    """KeyStorage manages Wireguard server key storage file (private and public keys)"""

    path: pathlib.PosixPath

    def __init__(self, path: str):
        self.path = pathlib.PosixPath(path)

    def exists(self):
        return self.path.exists()

    def _store(self, private_key: str, public_key: str):
        if not self.path.parent.exists():  # create parent directory if it doesn't exist
            self.path.parent.mkdir()

        with open(self.path, "x", encoding="utf-8") as file:
            json.dump({"private_key": private_key, "public_key": public_key}, file, indent=4)

    def generate_keys_and_store(self):
        private_key, public_key = generate_keypair()
        self._store(private_key, public_key)

    def read_keys(self) -> (str, str):
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data["private_key"], data["public_key"]
