from pycharm_debug_pymongo.util import get_registry
from pycharm_debug_pymongo.mongodb import MongoDatabase


def get_db(container, reset_connection=False):
    """
    Obtains the database connection from configured application settings.

    If :paramref:`reset_connection` is ``True``, the :paramref:`container` must be the application :class:`Registry` or
    any container that can retrieve it to accomplish reference reset. Otherwise, any settings container can be provided.
    """
    registry = get_registry(container, nothrow=True)
    if not reset_connection and registry and isinstance(getattr(registry, "db", None), MongoDatabase):
        return registry.db
    database = MongoDatabase(container)
    if reset_connection:
        registry = get_registry(container)
        registry.db = database
    return database


def includeme(config):
    def _add_db(request):
        return MongoDatabase(request)

    config.add_request_method(_add_db, "db", reify=True)
