from betterconf import Config as BaseConfig
from betterconf import field
from betterconf.caster import to_int


class Env(BaseConfig):
    """
    An interface for accessing configuration that was provided through environmental variables.
    """

    class Node(BaseConfig):
        _prefix_ = "NODE"

        # file which contains a root public key
        ROOT_API_USER_PUBLIC_KEY_FILE = field()

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
        USERNAME_FILE = field()
        PASSWORD_FILE = field()
        DATABASE_FILE = field()


env = Env()
