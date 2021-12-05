from http import HTTPStatus
from urllib.parse import urlparse, urljoin

from requests import post
from requests.auth import AuthBase
from requests.models import PreparedRequest

from wpclient.api.exceptions import AuthenticationFailure
from wpclient.api.singleton import Singleton


class JWTAuth(AuthBase, metaclass=Singleton):
    """
    Implements JWT authentication.

    Include the Authorization header with the JWT as value
    """

    auth_endpoint = "/wp-json/jwt-auth/v1/token"
    auth_validate_endpoint = "/wp-json/jwt-auth/v1/token/validate"

    def __init__(self, wp_url: str, wp_username: str, wp_password: str):
        self.wp_url = self.clean_url(wp_url)
        self.username = wp_username
        self.password = wp_password
        self._jwt: str

    @property
    def jwt(self) -> str:
        if not hasattr(self, "_jwt"):
            self._jwt = self._token()

        return self._jwt

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = "Bearer {token}".format(token=self.jwt)
        return r

    def clean_url(self, wp_url: str) -> str:
        """
        Check than wp_url is a valid URL and remove any path or trailing slash
        return: Cleaned URL
        """
        url = urlparse(wp_url)
        return "{scheme}://{netloc}".format(scheme=url.scheme, netloc=url.netloc)

    def _token(self) -> str:
        """
        Get Token by Authenticating using JWT protocol
        Set internal jwt property with obtained JWT
        return: JSON Web Token
        """
        url = urljoin(self.wp_url, self.auth_endpoint)
        data = {"username": self.username, "password": self.password}
        resp = post(url=url, data=data)

        if resp.status_code == HTTPStatus.OK:
            resp_json: dict = resp.json()
            return resp_json["token"]

        # Bad response
        msg = resp.json().get("message", "")
        exc_msg = "Authentication Failure. Status code: {0}. Message: {1}".format(
            resp.status_code, msg
        )
        raise AuthenticationFailure(exc_msg)
