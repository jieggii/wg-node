import re

from betterconf import Config as _Config
from betterconf import field
from betterconf.caster import to_int, AbstractCaster
from betterconf.exceptions import ImpossibleToCastError


class BaseAddressValidator(AbstractCaster):
    def cast(self, val: str):
        if not re.fullmatch(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.x$", val):
            raise ImpossibleToCastError(val, self)
        return val


class Config(_Config):
    class Mongo(_Config):
        _prefix_ = "MONGO_"

        HOST = field()
        PORT = field(caster=to_int)
        USER = field()
        PASSWORD = field()
        DATABASE = field()

    class WG:
        _prefix_ = "WG_"
        BASE_ADDRESS = field(caster=BaseAddressValidator())
        INTERFACE_LISTEN_PORT = field(caster=to_int)


config = Config()
