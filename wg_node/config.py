from betterconf import Config as _Config
from betterconf import field
from betterconf.caster import to_int

__all__ = ("config",)


class Config(_Config):
    class Node(_Config):
        _prefix_ = "NODE"

        # file which contains master's public keys
        MASTER_PUBLIC_KEYS_FILE = field()

    class Wireguard(_Config):
        _prefix_ = "WIREGUARD"

        # public hostname of the server
        HOSTNAME = field()

        # public UDP port being listened on the server
        PORT = field(caster=to_int)

    class Mongo(_Config):
        _prefix_ = "MONGO"

        HOST = field()
        PORT = field(caster=to_int)
        USERNAME_FILE = field()
        PASSWORD_FILE = field()
        DATABASE = field()


config = Config()
