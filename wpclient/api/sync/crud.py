from datetime import date, datetime
from http import HTTPStatus
from typing import Optional, Union
from urllib.parse import urljoin

from requests import Session

from wpclient.authentication.jwt import JWTAuth
from wpclient.api.exceptions import BadRequest
from wpclient.api.singleton import Singleton


class CRUD:
    api_base = "wp-json"
    _session = Session()

    def __init__(self, auth: JWTAuth) -> None:
        self._session.auth = auth
        self.wp_url = auth.wp_url

    @staticmethod
    def pre_parse_filters(
        filters: dict[str, Union[str, int, list[str, int]]]
    ) -> dict[str, str]:
        """
        Pre parse filters.

        The lists will be converted into text strings separated by commas.

        Numeric list values will be converted to text.
        """
        parsed_filters = {}

        for k, v in filters.items():
            parsed_filters[k] = (
                ",".join(list(map(str, v))) if isinstance(v, list) else v
            )

        return parsed_filters

    @classmethod
    def parse_filters(cls, filters: dict) -> str:
        """
        Parse filters

        Convert dictionary filters to URL query params string
        """
        pre_parsed = cls.pre_parse_filters(filters)

        return "&".join(list(map(lambda i: f"{i[0]}={i[1]}", pre_parsed.items())))

    def _filter(self, endpoint: str, filters: dict = {}) -> list[dict]:
        """
        Retrieve all objects matching the filters
        """

        url = self.assemble_url(endpoint)
        parsed_filters = self.parse_filters(filters)
        url = url + "?" + parsed_filters
        resp = self._session.get(url=url)

        if resp.status_code == HTTPStatus.OK:
            return resp.json()

        msg = f"\nFilters:\n{filters}\n\nResponse received:\n{resp.text}"
        raise BadRequest(msg)

    def assemble_url(self, endpoint: str, id: Optional[int] = None) -> str:
        """
        Join all API URL endpoint parts
        return: full endpoint URL
        """
        base_url = urljoin(self.wp_url, self.api_base)
        url = "{0}/{1}".format(base_url, endpoint.lstrip("/"))

        if id:
            url = "{0}/{1}".format(url.rstrip("/"), id)

        return url

    @staticmethod
    def datetime_to_str(dt: datetime) -> str:
        format = "%Y-%m-%dT%H:%M:%S"
        return dt.strftime(format)

    def _create(self, endpoint: str, data: dict) -> dict:
        """
        Create a new wp object
        """
        url = self.assemble_url(endpoint)
        resp = self._session.post(url=url, data=data)

        if resp.status_code == HTTPStatus.CREATED:
            return resp.json()

        msg = f"\nData sent:\n{data}\n\nResponse received:\n{resp.text}"
        raise BadRequest(msg)

    def _get(self, endpoint: str, id: int, filters: Optional[dict] = None) -> dict:
        """
        Retrieve a especific wp object by ID
        """
        url = self.assemble_url(endpoint, id)
        resp = self._session.get(url=url, params=filters)

        if resp.status_code == HTTPStatus.OK:
            return resp.json()

        raise BadRequest(resp.text)

    def _update(self, endpoint: str, id: int, data: dict) -> dict:
        """
        Update a wp object
        """

        url = self.assemble_url(endpoint, id)
        resp = self._session.post(url=url, data=data)

        if resp.status_code == HTTPStatus.OK:
            return resp.json()

        msg = f"\nData sent:\n{data}\n\nResponse received:\n{resp.text}"
        raise BadRequest(msg)

    def _delete(self, endpoint: str, id: int, force: bool = False) -> dict:
        """
        Delete a wp object
        """

        url = self.assemble_url(endpoint, id)
        resp = self._session.delete(url=url, data={"force": force})

        if resp.status_code == HTTPStatus.OK:
            return resp.json()

        raise BadRequest(resp.text)
