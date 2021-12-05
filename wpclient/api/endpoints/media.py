from asyncio.locks import Semaphore
from pathlib import Path
from typing import Literal, Optional

from aiohttp.client import ClientSession
from wpclient.api.exceptions import MediaSourceNotProvided

from wpclient.models.media import MediaModel, MediaFilter
from .crud import CRUD


class Media(CRUD):
    endpoint = "/wp/v2/media"

    def __init__(self, session: ClientSession, sem: Semaphore) -> None:
        self.semaphore = sem
        self.session = session

    async def filter(self, filter: MediaFilter) -> list[MediaModel]:
        """
        Retrieve all media matching the filter
        """

        filters: dict = filter.dict(exclude_none=True)

        async with self.semaphore:
            objects: list[dict] = await self._filter(
                session=self.session, endpoint=self.endpoint, filters=filters
            )

            return [MediaModel.parse_obj(obj) for obj in objects]

    async def create(self, media: MediaModel) -> MediaModel:
        """
        Create a new media
        """
        if not media.source:
            raise MediaSourceNotProvided

        filename = Path(media.source).name
        self.session.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{filename}"'
        data: dict = media.dict(exclude_none=True, exclude={"source"})

        with open(media.source, "rb") as f:

            data["file"] = f

            async with self.semaphore:
                wp_obj: dict = await self._create(
                    session=self.session, endpoint=self.endpoint, body=data
                )
                print(wp_obj)

                return media.parse_obj(wp_obj)

    async def get(
        self, id: int, context: Optional[Literal["view", "embed", "edit"]] = None
    ) -> MediaModel:
        """
        Retrieve a especific media by ID
        """

        filters = {}

        if context:
            filters["context"] = context

        async with self.semaphore:
            wp_obj: dict = await self._get(
                session=self.session, endpoint=self.endpoint, id=id, filters=filters
            )

            return MediaModel.parse_obj(wp_obj)

    async def update(self, id: int, data: dict) -> MediaModel:
        """
        Update a media
        """

        async with self.semaphore:
            wp_obj: dict = await self._update(
                session=self.session, endpoint=self.endpoint, id=id, data=data
            )

            return MediaModel.parse_obj(wp_obj)

    async def delete(self, id: int) -> bool:
        """
        Delete a media
        """
        async with self.semaphore:
            wp_obj: dict = await self._delete(
                session=self.session, endpoint=self.endpoint, id=id, force=True
            )

            return wp_obj["deleted"]
