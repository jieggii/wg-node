import json
import pathlib

from .key import generate_keypair


class KeyStorage:
    """KeyStorage manages Wireguard server key storage file (private and public keys)"""
    _path: pathlib.PosixPath

    def __init__(self, path: str):
        self._path = pathlib.PosixPath(path)

    def exists(self) -> bool:
        """Returns True if key storage file exists, otherwise False"""
        return self._path.exists()

    def store_keys(self, *, private_key: str, public_key: str) -> None:
        """
        Stores private and public key in file (self._path)
        Note: can be called only once for one storage path, raises FileExistsError
        if storage file already exists.
        """

        if not self._path.parent.exists():  # create parent directory if it doesn't exist
            self._path.parent.mkdir()

        with open(self._path, "x", encoding="utf-8") as file:
            json.dump({"private_key": private_key, "public_key": public_key}, file, indent=4)

    def read_keys(self) -> (str, str):
        """Reads and returns private and public keys from the storage file."""
        with open(self._path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data["private_key"], data["public_key"]
