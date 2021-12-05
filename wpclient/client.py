import asyncio
from collections.abc import Coroutine
from types import TracebackType
from typing import Any, Optional, Type

from aiohttp import ClientSession

from wpclient.api.endpoints.posts import Posts
from wpclient.api.endpoints.categories import Categories
from wpclient.api.endpoints.tags import Tags
from wpclient.api.endpoints.media import Media
from wpclient.api.endpoints.pages import Pages
from wpclient.authentication.jwt import JWTAuth
from wpclient.api.functions import clean_url


class Client:

    endpoints = {
        "posts": Posts,
        "categories": Categories,
        "tags": Tags,
        "media": Media,
        "pages": Pages,
    }

    def __init__(
        self, wp_url: str, wp_username: str, wp_password: str, max_con: int = 100
    ):
        self.wp_url = wp_url
        self.wp_username = wp_username
        self.wp_password = wp_password
        self.sempahore = asyncio.Semaphore(max_con)
        self.tasks: list[Coroutine] = []
        self.result: Optional[Any] = None
        self.posts: Posts
        self.categories: Categories
        self.tags: Tags
        self.media: Media
        self.pages: Pages
        self.session: ClientSession

    async def perform(self):
        if self.tasks:
            self.result = await asyncio.gather(*self.tasks)

    def add(self, coro: Coroutine):
        self.tasks.append(asyncio.create_task(coro))

    async def get_session(self):
        base_url = clean_url(self.wp_url)
        auth = JWTAuth(self.wp_url, self.wp_username, self.wp_password)
        headers = {"Authorization": f"Bearer {auth.jwt}"}
        self.session = await ClientSession(
            base_url=base_url, headers=headers
        ).__aenter__()

    async def __aenter__(self) -> "Client":
        await self.get_session()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if not self.session.closed:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)

    def _init_endpoint(self, name: str):
        """
        Initialize a WP endpoint class
        Set the endpoint instance as class atrribute
        """
        _class = self.endpoints[name]
        instance = _class(self.session, self.sempahore)
        setattr(self, name, instance)

    def __getattr__(self, attr: str):
        if attr in self.endpoints:
            self._init_endpoint(attr)
            return getattr(self, attr)

        raise AttributeError(f"WP API has no '{attr}' endpoint")
