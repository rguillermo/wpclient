from pathlib import Path
import pytest


@pytest.fixture
def auth_data():
    return {
        'wp_url': 'http://127.0.0.1:8000/',
        'wp_username': 'admin',
        'wp_password': 'admin'
    }


@pytest.fixture
def post_data():
    return {
        'title': 'My post title',
        'content': 'Post content',
    }


@pytest.fixture
def category_data():
    return {
        'name': 'My awesome category',
        'description': 'My category nice description'
    }


@pytest.fixture
def tag_data():
    return {
        'name': 'My awesome Tag',
        'description': 'My tag nice description'
    }


@pytest.fixture
def media_data():
    return {
        'alt_text': 'My custom alt text',
        'source': str(Path('tests/sample.png').resolve())
    }


@pytest.fixture
def page_data():
    return {
        'title': 'My page title',
        'content': 'Page content',
    }