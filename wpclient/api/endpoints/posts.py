from asyncio.locks import Semaphore
from typing import Literal, Optional

from aiohttp import ClientSession

from wpclient.api.endpoints.crud import CRUD
from wpclient.models.post import Post, PostFilter


class Posts(CRUD):
    endpoint = "/wp/v2/posts"

    def __init__(self, session: ClientSession, sem: Semaphore) -> None:
        self.session = session
        self.semaphore = sem

    async def filter(self, filter: PostFilter) -> list[Post]:
        """
        Retrieve all posts matching the filter
        """

        filters: dict = filter.dict(exclude_none=True)
        async with self.semaphore:
            objects: list[dict] = await self._filter(
                session=self.session, endpoint=self.endpoint, filters=filters
            )

            return [Post.parse_obj(obj) for obj in objects]

    async def create(self, post: Post) -> Post:
        """
        Create a post
        """
        data: dict = post.dict(exclude_none=True)

        async with self.semaphore:
            wp_post: dict = await self._create(
                session=self.session, endpoint=self.endpoint, data=data
            )
            return post.parse_obj(wp_post)

    async def get(
        self,
        id: int,
        context: Optional[Literal["view", "embed", "edit"]] = None,
        password: Optional[str] = None,
    ) -> Post:
        """
        Retrieve a specific post
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
            post = Post.parse_obj(post_data)

            return post

    async def update(self, id: int, data: dict) -> Post:
        """
        Update a post with the given kwargs
        """
        async with self.semaphore:
            wp_obj: dict = await self._update(
                session=self.session, endpoint=self.endpoint, id=id, data=data
            )

            return Post.parse_obj(wp_obj)

    async def delete(self, id: int, force: bool = True) -> bool:
        """
        Delete a post
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
