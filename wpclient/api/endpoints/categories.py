from asyncio.locks import Semaphore
from typing import Literal, Optional

from aiohttp.client import ClientSession

from wpclient.models.category import Category, CategoryFilter
from .crud import CRUD


class Categories(CRUD):
    endpoint = "/wp/v2/categories"

    def __init__(self, session: ClientSession, sem: Semaphore) -> None:
        self.semaphore = sem
        self.session = session

    async def filter(self, filter: CategoryFilter) -> list[Category]:
        """
        Retrieve all categories matching the filter
        """

        filters: dict = filter.dict(exclude_none=True)

        async with self.semaphore:
            objects: list[dict] = await self._filter(
                session=self.session, endpoint=self.endpoint, filters=filters
            )

            return [Category.parse_obj(obj) for obj in objects]

    async def create(self, category: Category) -> Category:
        """
        Create a new category
        """
        data: dict = category.dict(exclude_none=True)

        async with self.semaphore:
            wp_obj: dict = await self._create(
                session=self.session, endpoint=self.endpoint, data=data
            )

            return category.parse_obj(wp_obj)

    async def get(
        self, id: int, context: Optional[Literal["view", "embed", "edit"]] = None
    ) -> Category:
        """
        Retrieve a especific category by ID
        """

        filters = {}

        if context:
            filters["context"] = context

        async with self.semaphore:
            wp_obj: dict = await self._get(
                session=self.session, endpoint=self.endpoint, id=id, filters=filters
            )

            return Category.parse_obj(wp_obj)

    async def update(self, id: int, data: dict) -> Category:
        """
        Update a category
        """

        async with self.semaphore:
            wp_obj: dict = await self._update(
                session=self.session, endpoint=self.endpoint, id=id, data=data
            )

            return Category.parse_obj(wp_obj)

    async def delete(self, id: int) -> bool:
        """
        Delete a category
        """
        async with self.semaphore:
            wp_obj: dict = await self._delete(
                session=self.session, endpoint=self.endpoint, id=id, force=True
            )

            return wp_obj["deleted"]
