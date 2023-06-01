from .repository import ConfigRepository
from sqlalchemy.exc import SQLAlchemyError


class ConfigProcessor:
    """
    Basic work with configuration stored somewhere in db
    """

    internal_cache = {}

    def __init__(self):
        self.repository = ConfigRepository()

    def sync(self):
        ConfigProcessor.internal_cache = {}
        for rec in self.repository.read_all():
            ConfigProcessor.internal_cache[rec.key] = rec.value

    def get(self, key: str):
        if key not in ConfigProcessor.internal_cache.keys():
            try:
                rec = self.repository.read(key)
            except SQLAlchemyError:
                return None
            ConfigProcessor.internal_cache[key] = rec.value
        return ConfigProcessor.internal_cache[key]

    def set(self, key: str, value):
        saved = self.repository.read(key)
        if saved:
            # found - update/delete
            if value is None:
                self.repository.delete(key)
            else:
                self.repository.update(key, value)
        else:
            # nothing found - will add
            if value is not None:
                self.repository.add(key, value)
        ConfigProcessor.internal_cache[key] = value


class AConfigKeys:
    """
    The key-value pair itself as an object
    """

    def __init__(self):
        self.processor = ConfigProcessor()
        self.processor.sync()

    def get(self) -> str:
        stored = self.processor.get(self._which_key())
        return str(stored) if stored is not None else ''

    def set(self, value: str):
        self.processor.set(self._which_key(), value)

    def _which_key(self) -> str:
        raise NotImplementedError('TBA')


class ConfigToken(AConfigKeys):
    """
    Token from initial query, necessary for work with rest of the remote queries
    """

    instance = None

    @staticmethod
    def static():
        if not ConfigToken.instance:
            ConfigToken.instance = ConfigToken()
        return ConfigToken.instance

    def _which_key(self) -> str:
        return 'known_token'


class ConfigAdmin(AConfigKeys):
    """
    Master token to process enabled users allowed to work with other users
    """

    instance = None

    @staticmethod
    def static():
        if not ConfigAdmin.instance:
            ConfigAdmin.instance = ConfigAdmin()
        return ConfigAdmin.instance

    def _which_key(self) -> str:
        return 'known_admin'
