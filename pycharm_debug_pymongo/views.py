from pycharm_debug_pymongo.db import get_db
from pyramid.httpexceptions import HTTPBadRequest, HTTPConflict, HTTPOk, HTTPNotFound
from time import sleep


def sleep_query(request, name):
    try:
        time = request.params.get(name)
        if time:
            time = int(time)
            sleep(time)
    except ValueError:
        return HTTPBadRequest(json={"message": f"incorrect '{name}' must be a number of seconds"})


def get_service(request):
    name = request.matchdict.get("name")
    store = get_db(request).get_store()
    sleep_query(request, "sleep-before")
    try:
        service = store.fetch_by_name(name)
        if not service:
            return HTTPNotFound(json={"message": "service not found"})
        sleep_query(request, "sleep-after")
        return HTTPOk(json=service)
    except ValueError:
        return HTTPNotFound(json={"message": "service not found"})


def post_service(request):
    try:
        name = request.json["name"]
        if not name:
            raise ValueError
    except (KeyError, ValueError):
        return HTTPBadRequest(json={"message": "missing service name"})
    store = get_db(request).get_store()
    service = store.fetch_by_name(name)
    if service:
        return HTTPConflict(json={"message": "service already exists"})
    store.save_service({"name": name})
    service = store.fetch_by_name(name)
    body = {"message": "Service created"}
    body.update({"service": service})
    return HTTPOk(json=body)


def delete_service(request):
    name = request.matchdict.get("name")
    store = get_db(request).get_store()
    try:
        ok = store.delete_service(name)
        if not ok:
            return HTTPNotFound(json={"message": "service not found"})
        return HTTPOk(json={"message": "Service deleted."})
    except ValueError:
        return HTTPNotFound(json={"message": "service not found"})


def list_services(request):
    store = get_db(request).get_store()
    services = store.list_services()
    return HTTPOk(json=services)


def get_frontpage(request):
    return HTTPOk(json={"message": "WebApp service is working!"})
