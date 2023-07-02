from os.path import exists
from typing import NoReturn

from betterconf import Config as BaseConfig
from betterconf import field
from betterconf.caster import to_int
from betterconf.config import AbstractCaster  # noqa

__all__ = ("config",)


class ToExistingPathCaster(AbstractCaster):
    def cast(self, val: str) -> str | NoReturn:
        if not exists(val):
            raise FileNotFoundError(f"file {val} does not exist")
        return val


to_existing_path_caster = ToExistingPathCaster()


class Config(BaseConfig):
    """
    An interface for accessing configuration that was provided through environmental variables.
    """

    class Node(BaseConfig):
        _prefix_ = "NODE"

        # file which contains a root public key
        ROOT_API_USER_PUBLIC_KEY_FILE = field(caster=to_existing_path_caster)

    class Wireguard(BaseConfig):
        _prefix_ = "WIREGUARD"

        # public hostname of the server
        PUBLIC_HOSTNAME = field()

        # public UDP port being listened on the server
        PUBLIC_PORT = field(caster=to_int)

    class Mongo(BaseConfig):
        _prefix_ = "MONGO"

        HOST = field()
        PORT = field(caster=to_int)
        USERNAME_FILE = field(caster=to_existing_path_caster)
        PASSWORD_FILE = field(caster=to_existing_path_caster)
        DATABASE_FILE = field(caster=to_existing_path_caster)


config = Config()
