from http import HTTPStatus
from typing import Optional

from aiohttp import ClientSession

from wpclient.api.exceptions import BadRequest
from wpclient.api.functions import assemble_url, parse_filters


class CRUD:
    async def _filter(
        self, session: ClientSession, endpoint: str, filters: dict = {}
    ) -> list[dict]:
        """
        Retrieve all objects matching the filters
        """

        parsed_filters = parse_filters(filters)
        url = "/wp-json" + endpoint + "?" + parsed_filters

        async with session.get(url=url) as resp:

            if resp.status == HTTPStatus.OK:
                return await resp.json()

            msg = f"\nFilters:\n{filters}\n\nResponse received:\n{await resp.text()}"
            raise BadRequest(msg)

    async def _create(
        self,
        session: ClientSession,
        endpoint: str,
        data: Optional[dict] = None,
        body=None,
    ) -> dict:
        """
        Create a new wp object
        """

        url = assemble_url(endpoint)

        async with session.post(url=url, json=data, data=body) as resp:

            if resp.status == HTTPStatus.CREATED:
                return await resp.json()

            msg = f"\nData sent:\n{data}\n\nResponse received:\n{await resp.text()}"
            raise BadRequest(msg)

    async def _get(
        self,
        session: ClientSession,
        endpoint: str,
        id: int,
        filters: Optional[dict] = None,
    ) -> dict:
        """
        Retrieve a especific wp object by ID
        """

        url = assemble_url(endpoint, id)

        async with session.get(url=url, params=filters) as resp:

            if resp.status == HTTPStatus.OK:
                return await resp.json()

            raise BadRequest(await resp.text())

    async def _update(
        self, session: ClientSession, endpoint: str, id: int, data: dict
    ) -> dict:
        """
        Update a wp object
        """

        url = "/wp-json" + endpoint + "/" + str(id)

        async with session.post(url=url, json=data) as resp:

            if resp.status == HTTPStatus.OK:
                return await resp.json()

            msg = f"\nData sent:\n{data}\n\nResponse received:\n{await resp.text()}"
            raise BadRequest(msg)

    async def _delete(
        self, session: ClientSession, endpoint: str, id: int, force: bool = False
    ) -> dict:
        """
        Delete a wp object
        """

        url = assemble_url(endpoint, id)

        async with session.delete(url=url, data={"force": force}) as resp:

            if resp.status == HTTPStatus.OK:
                return await resp.json()

            raise BadRequest(await resp.text())
