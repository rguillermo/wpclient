from asyncio.locks import Semaphore
from typing import Literal, Optional

from aiohttp import ClientSession

from wpclient.api.endpoints.crud import CRUD
from wpclient.models.page import Page, PageFilter


class Pages(CRUD):
    endpoint = "/wp/v2/pages"

    def __init__(self, session: ClientSession, sem: Semaphore) -> None:
        self.session = session
        self.semaphore = sem

    async def filter(self, filter: PageFilter) -> list[Page]:
        """
        Retrieve all posts matching the filter
        """

        filters: dict = filter.dict(exclude_none=True)
        async with self.semaphore:
            objects: list[dict] = await self._filter(
                session=self.session, endpoint=self.endpoint, filters=filters
            )

            return [Page.parse_obj(obj) for obj in objects]

    async def create(self, page: Page) -> Page:
        """
        Create a page
        """
        data: dict = page.dict(exclude_none=True)

        async with self.semaphore:
            wp_post: dict = await self._create(
                session=self.session, endpoint=self.endpoint, data=data
            )
            return page.parse_obj(wp_post)

    async def get(
        self,
        id: int,
        context: Optional[Literal["view", "embed", "edit"]] = None,
        password: Optional[str] = None,
    ) -> Page:
        """
        Retrieve a specific page
        """
        filters = {}

        if context:
            filters["context"] = context

        if password:
            filters["password"] = password

        async with self.semaphore:
            post_data: dict = await self._get(
                session=self.session, endpoint=self.endpoint, id=id, filters=filters
            )
            page = Page.parse_obj(post_data)

            return page

    async def update(self, id: int, data: dict) -> Page:
        """
        Update a page with the given kwargs
        """
        async with self.semaphore:
            wp_obj: dict = await self._update(
                session=self.session, endpoint=self.endpoint, id=id, data=data
            )

            return Page.parse_obj(wp_obj)

    async def delete(self, id: int, force: bool = True) -> bool:
        """
        Delete a page
        """
        async with self.semaphore:
            wp_obj = await self._delete(
                session=self.session, endpoint=self.endpoint, id=id, force=force
            )

            if force:
                return wp_obj["deleted"]

            if wp_obj["id"]:
                return True

            return False
