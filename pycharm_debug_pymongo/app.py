#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyramid.config import Configurator


def main(global_config, **settings):
    """
    Creates a Pyramid WSGI application.
    """
    local_config = Configurator(settings=settings)
    if global_config.get("__file__") is not None:
        local_config.include("pyramid_celery")
        local_config.configure_celery(global_config["__file__"])
    local_config.include("pycharm_debug_pymongo")
    return local_config.make_wsgi_app()
