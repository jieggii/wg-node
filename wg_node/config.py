from betterconf import Config as _Config
from betterconf import field
from betterconf.caster import to_int

__all__ = ("config",)


class Config(_Config):
    class Node(_Config):
        _prefix_ = "NODE"

        # secret key which is used to authorize every API call
        SECRET_KEY = field()

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
        USER = field()
        PASSWORD = field()
        DATABASE = field()


config = Config()
