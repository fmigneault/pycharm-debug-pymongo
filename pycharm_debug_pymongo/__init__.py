from pycharm_debug_pymongo import views


def includeme(config):
    config.add_route(name="get_frontpage", pattern="/")
    config.add_view(views.get_frontpage, route_name="get_frontpage", request_method="GET", renderer="json")

    config.add_route(name="list_services", pattern="/services", request_method="GET")
    config.add_view(views.list_services, route_name="list_services", request_method="GET", renderer="json")

    config.add_route(name="post_service", pattern="/services", request_method="POST")
    config.add_view(views.post_service, route_name="post_service", request_method="POST", renderer="json")

    config.add_route(name="get_service", pattern="/services/{name}", request_method="GET")
    config.add_view(views.get_service, route_name="get_service", request_method="GET", renderer="json")

    config.add_route(name="delete_service", pattern="/services/{name}", request_method="DELETE")
    config.add_view(views.delete_service, route_name="delete_service", request_method="DELETE", renderer="json")
