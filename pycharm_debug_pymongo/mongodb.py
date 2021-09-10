import pymongo
import warnings
from pycharm_debug_pymongo.util import get_settings
from pycharm_debug_pymongo.store import MongodbServiceStore


class MongoDatabase(object):
    _database = None
    _settings = None
    _stores = None
    type = "mongodb"

    def __init__(self, container):
        settings = get_settings(container)
        self._database = get_mongodb_engine(settings)
        self._settings = settings
        self._stores = dict()

    def get_store(self, *store_args, **store_kwargs):
        """
        Retrieve a store from the database.

        :param store_args: additional arguments to pass down to the store.
        :param store_kwargs: additional keyword arguments to pass down to the store.
        """
        store = self._stores.get("services")
        if not store:
            self._stores["services"] = store = MongodbServiceStore(
                collection=getattr(self.get_session(), "services"),
                *store_args, **store_kwargs
            )
        return store

    def get_session(self):
        return self._database

    def get_information(self):
        """
        Obtain information about the database implementation.

        :returns: JSON with parameters: ``{"version": "<version>", "type": "<db_type>"}``.
        """
        result = list(self._database.version.find().limit(1))[0]
        db_version = result["version_num"]
        return {"version": db_version, "type": self.type}

    def is_ready(self):
        # type: (...) -> bool
        return self._database is not None and self._settings is not None


def get_mongodb_connection(container):
    """
    Obtains the basic database connection from settings.
    """
    settings = get_settings(container)
    settings_default = [
        ("mongodb.host", "localhost"),
        ("mongodb.port", 27017),
        ("mongodb.db_name", "pycharm_debug_pymongo")
    ]
    for setting, default in settings_default:
        if settings.get(setting, None) is None:
            warnings.warn("Setting '{}' not defined in registry, using default [{}].".format(setting, default))
            settings[setting] = default
    client = pymongo.MongoClient(settings["mongodb.host"], int(settings["mongodb.port"]), connect=True)
    return client[settings["mongodb.db_name"]]


def get_mongodb_engine(container):
    """
    Obtains the database with configuration ready for usage.
    """
    db = get_mongodb_connection(container)
    db.services.create_index("name", unique=True)
    return db
