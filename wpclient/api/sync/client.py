from importlib import import_module

from wpclient.authentication.jwt import JWTAuth
from wpclient.api.sync import *


class WPAPI:
    """
    Composition class of all available WordPress API endpoints

    WP endpoints are imported and initialized lazily as needed
    """

    endpoints = {
        "posts",
        "categories",
    }

    _endpoints_pkg = "wpclient.api.sync"

    def __init__(self, wp_url: str, wp_username: str, wp_password: str) -> None:
        self.auth = JWTAuth(wp_url, wp_username, wp_password)
        self.posts: Posts
        self.categories: Categories

    def _import_endpoint_module(self, name: str):
        """
        Import a WP endpoint module
        return: Imported module
        """
        module_path = f"{self._endpoints_pkg}.{name}"

        return import_module(module_path)

    def _init_endpoint(self, name: str):
        """
        Initialize a WP endpoint class
        Set the endpoint instance as class atrribute
        """
        module = self._import_endpoint_module(name)
        classname = name.capitalize()
        _class = getattr(module, classname)
        instance = _class(self.auth)
        setattr(self, name, instance)

    def __getattr__(self, attr: str):
        if attr in self.endpoints:
            self._init_endpoint(attr)
            return getattr(self, attr)

        raise AttributeError(f"WP API has no '{attr}' endpoint")
