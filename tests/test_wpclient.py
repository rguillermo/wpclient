#!/usr/bin/env python

"""Tests for `wpclient` package."""

import pytest

from wpclient.api.sync.client import WPAPI
from wpclient.api.sync.posts import Posts
from wpclient.api.sync.categories import Categories


@pytest.fixture
def auth_data():
    return {
        'wp_url': 'http://127.0.0.1:8000/',
        'wp_username': 'admin',
        'wp_password': 'admin'
    }



def test_wpapi_can_instantiate(auth_data):
    api = WPAPI(**auth_data)
    assert isinstance(api, WPAPI)


def test_wpapi_lazy_endpoints(auth_data):
    api = WPAPI(**auth_data)
    assert hasattr(api, 'posts')
    assert hasattr(api, 'categories')
    assert isinstance(api.posts, Posts)
    assert isinstance(api.categories, Categories)


def test_wpapi_raise_exception_on_not_registered_endpoint(auth_data):
    api = WPAPI(**auth_data)
    with pytest.raises(AttributeError):
        api.bad_endpoint


def test_wpapi_reusing_crud_instance(auth_data):
    api = WPAPI(**auth_data)
    assert api.posts._session is api.categories._session
    assert api.posts._session.auth is api.categories._session.auth

