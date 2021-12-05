from datetime import datetime
from typing import Optional, Union
from urllib.parse import urljoin, urlparse

from aiohttp import ClientSession
from wpclient.authentication.jwt import JWTAuth


async def get_session(wp_url, wp_username, wp_password):
    base_url = clean_url(wp_url)
    auth = JWTAuth(wp_url, wp_username, wp_password)
    headers = {"Authorization": f"Bearer {auth.jwt}"}
    async with ClientSession(base_url=base_url, headers=headers) as session:
        return session


def clean_url(wp_url: str) -> str:
    """
    Check than wp_url is a valid URL and remove any path or trailing slash
    return: Cleaned URL
    """
    url = urlparse(wp_url)
    return "{scheme}://{netloc}".format(scheme=url.scheme, netloc=url.netloc)


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
        parsed_filters[k] = ",".join(list(map(str, v))) if isinstance(v, list) else v

    return parsed_filters


def parse_filters(filters: dict) -> str:
    """
    Parse filters

    Convert dictionary filters to URL query params string
    """
    pre_parsed = pre_parse_filters(filters)

    return "&".join(list(map(lambda i: f"{i[0]}={i[1]}", pre_parsed.items())))


def assemble_url(
    endpoint: str, id: Optional[int] = None, filters: Optional[dict] = None
) -> str:
    """
    Join all API URL endpoint parts
    return: full endpoint URL
    """
    base = "/wp-json"
    url = "{0}/{1}".format(base, endpoint.lstrip("/"))

    if id:
        url = "{0}/{1}".format(url.rstrip("/"), id)

    if filters:
        parsed_filters = parse_filters(filters)
        url += f"?{parsed_filters}"

    return url


def datetime_to_str(dt: datetime) -> str:
    format = "%Y-%m-%dT%H:%M:%S"

    return dt.strftime(format)
