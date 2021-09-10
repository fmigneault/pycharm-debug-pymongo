from pyramid.request import Request
from pyramid.config import Configurator
from pyramid.registry import Registry
from pyramid.threadlocal import get_current_registry
from celery import Celery


def get_registry(container, nothrow=False):
    """
    Retrieves the application ``registry`` from various containers referencing to it.
    """
    if isinstance(container, Celery):
        return container.conf.get("PYRAMID_REGISTRY", {})
    if isinstance(container, (Configurator, Request)):
        return container.registry
    if isinstance(container, Registry):
        return container
    if nothrow:
        return None
    raise TypeError("Could not retrieve registry from container object of type [{}].".format(type(container)))


def get_settings(container=None):
    """
    Retrieves the application ``settings`` from various containers referencing to it.
    """
    if isinstance(container, (Celery, Configurator, Request)):
        container = get_registry(container)
    if isinstance(container, Registry):
        return container.settings
    if isinstance(container, dict):
        return container
    if container is None:
        return get_current_registry().settings
    raise TypeError("Could not retrieve settings from container object of type [{}]".format(type(container)))
