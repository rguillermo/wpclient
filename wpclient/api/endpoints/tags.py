from asyncio.locks import Semaphore
from typing import Literal, Optional

from aiohttp.client import ClientSession

from wpclient.models.tag import Tag, TagFilter
from .crud import CRUD


class Tags(CRUD):
    endpoint = "/wp/v2/tags"

    def __init__(self, session: ClientSession, sem: Semaphore) -> None:
        self.semaphore = sem
        self.session = session

    async def filter(self, filter: TagFilter) -> list[Tag]:
        """
        Retrieve all tags matching the filter
        """

        filters: dict = filter.dict(exclude_none=True)

        async with self.semaphore:
            objects: list[dict] = await self._filter(
                session=self.session, endpoint=self.endpoint, filters=filters
            )

            return [Tag.parse_obj(obj) for obj in objects]

    async def create(self, tag: Tag) -> Tag:
        """
        Create a new tag
        """
        data: dict = tag.dict(exclude_none=True)

        async with self.semaphore:
            wp_obj: dict = await self._create(
                session=self.session, endpoint=self.endpoint, data=data
            )

            return tag.parse_obj(wp_obj)

    async def get(
        self, id: int, context: Optional[Literal["view", "embed", "edit"]] = None
    ) -> Tag:
        """
        Retrieve a especific tag by ID
        """

        filters = {}

        if context:
            filters["context"] = context

        async with self.semaphore:
            wp_obj: dict = await self._get(
                session=self.session, endpoint=self.endpoint, id=id, filters=filters
            )

            return Tag.parse_obj(wp_obj)

    async def update(self, id: int, data: dict) -> Tag:
        """
        Update a tag
        """

        async with self.semaphore:
            wp_obj: dict = await self._update(
                session=self.session, endpoint=self.endpoint, id=id, data=data
            )

            return Tag.parse_obj(wp_obj)

    async def delete(self, id: int) -> bool:
        """
        Delete a tag
        """
        async with self.semaphore:
            wp_obj: dict = await self._delete(
                session=self.session, endpoint=self.endpoint, id=id, force=True
            )

            return wp_obj["deleted"]
