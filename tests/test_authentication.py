import pytest

from wpclient.authentication.jwt import JWTAuth
from wpclient.api.exceptions import AuthenticationFailure


@pytest.fixture
def auth_data():
    return {
        'wp_url': 'http://127.0.0.1:8000/',
        'wp_username': 'admin',
        'wp_password': 'admin'
    }


@pytest.fixture
def bad_auth_data():
    return {
        'wp_url': 'http://127.0.0.1:8000/',
        'wp_username': 'admin',
        'wp_password': 'bad_password'
    }


def test_jwt_auth(auth_data: dict):
    auth = JWTAuth(**auth_data)
    assert type(auth.jwt) == str


def test_jwt_singleton(bad_auth_data: dict, auth_data: dict):
    auth1 = JWTAuth(**auth_data)
    auth2 = JWTAuth(**bad_auth_data)
    assert auth1 is auth2
