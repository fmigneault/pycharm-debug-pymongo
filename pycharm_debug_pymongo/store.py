import pymongo
from pymongo.collection import Collection
from typing import Any, Dict, List, Optional, Tuple


class MongodbStore(object):
    """
    Base class extended by all concrete store implementations.
    """

    def __init__(self, collection, sane_name_config=None):
        # type: (Collection, Optional[Dict[str, Any]]) -> None
        if not isinstance(collection, pymongo.collection.Collection):
            raise TypeError("Collection not of expected type.")
        self.collection = collection  # type: Collection
        self.sane_name_config = sane_name_config or {}

    @classmethod
    def get_args_kwargs(cls, *args, **kwargs):
        # type: (*Any, **Any) -> Tuple[Tuple, Dict]
        """
        Filters :class:`MongodbStore`-specific arguments to safely pass them down its ``__init__``.
        """
        collection = None
        if len(args):
            collection = args[0]
        elif "collection" in kwargs:    # pylint: disable=R1715
            collection = kwargs["collection"]
        sane_name_config = kwargs.get("sane_name_config", None)
        return tuple([collection]), {"sane_name_config": sane_name_config}


class MongodbServiceStore(MongodbStore):
    """
    Registry for OWS services.

    Uses `MongoDB` to store service url and attributes.
    """

    def __init__(self, *args, **kwargs):
        db_args, db_kwargs = MongodbStore.get_args_kwargs(*args, **kwargs)
        MongodbStore.__init__(self, *db_args, **db_kwargs)

    def save_service(self, service, overwrite=True):
        # type: (Dict, bool) -> Dict
        """
        Stores an OWS service in mongodb.
        """
        service_name = service.get("name")
        if self.collection.count_documents({"name": service_name}) > 0:
            if overwrite:
                self.collection.delete_one({"name": service_name})
            else:
                raise ValueError("service name already registered.")
        result = self.collection.insert_one({"name": service_name})
        return {"id": str(result.inserted_id), "name": service_name}

    def delete_service(self, name):
        # type: (str) -> bool
        """
        Removes service from `MongoDB` storage.
        """
        result = self.collection.delete_one({"name": name})
        return result.deleted_count == 1

    def fetch_by_name(self, name):
        # type: (str) -> Optional[Dict]
        """
        Gets service for given ``name`` from `MongoDB` storage.
        """
        service = self.collection.find_one({"name": name})
        if not service:
            return None
        service["id"] = str(service.pop("_id"))
        return service

    def list_services(self):
        # type: () -> List[Dict]
        """
        Lists all services in `MongoDB` storage.
        """
        services = []
        for service in self.collection.find().sort("name", pymongo.ASCENDING):
            service["id"] = str(service.pop("_id"))
            services.append(service)
        return services
