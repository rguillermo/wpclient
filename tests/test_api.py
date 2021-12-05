import random
from datetime import datetime

import pytest
from wpclient.api.sync.categories import Categories

from wpclient.authentication.jwt import JWTAuth
from wpclient.models.category import Category, CategoryFilter
from wpclient.api.sync.posts import Posts
from wpclient.models.post import Post, PostFilter


@pytest.fixture
def auth_data():
    return {
        'wp_url': 'http://127.0.0.1:8000/',
        'wp_username': 'admin',
        'wp_password': 'admin'
    }

@pytest.fixture
def post_data():
    return Post(
        title='New post title',
        content='New post content',
        date=datetime.now(),
        slug='my-custom-slug'
    )

@pytest.fixture
def category_data():
    category = Category(name='My category name')
    category.description = 'My category description'
    category.slug = 'my-custom-category-slug'
    return category

@pytest.fixture
def auth(auth_data):
    return JWTAuth(**auth_data)


def test_crud_post(auth, post_data):
    posts = Posts(auth)

    # Create
    post = posts.create(post_data)
    assert isinstance(post, Post)
    assert isinstance(post.id, int)

    # Filter
    post_ids = [post.id]
    for _ in range(3):
        p = posts.create(post_data)
        post_ids.append(p.id)

    # choice 3 random post ids for filter
    filter_include = PostFilter(include=random.sample(post_ids, 3))
    filtered = posts.filter(filter_include)
    assert len(filtered) == 3
    filter_exclude = PostFilter(exclude=random.sample(post_ids, 3))
    filtered = posts.filter(filter_exclude)
    assert len(filtered) == 1


    # Read
    post = posts.get(post.id)
    assert isinstance(post, Post)

    # Update
    new_title = 'My new title'
    post = posts.update(post.id, {'title': new_title})
    assert isinstance(post, Post)
    assert post.title == new_title

    # Delete
    for id in post_ids:
        post_id = posts.delete(id)
        assert isinstance(post_id, int)

    filter = PostFilter()
    filter.include = post_ids
    filtered = posts.filter(filter)
    assert len(filtered) == 0


def test_crud_category(auth, category_data):
    categories = Categories(auth)

    # Create
    cat = categories.create(category_data)
    assert isinstance(cat, Category)
    assert isinstance(cat.id, int)

    # Filter
    cat_ids = [cat.id]
    for i in range(2):
        category_data.name += str(i)
        category_data.slug += str(i)
        cat = categories.create(category_data)
        cat_ids.append(cat.id)

    # choice 2 random post ids for filter
    filter_include = CategoryFilter(include=random.sample(cat_ids, 2))
    filtered = categories.filter(filter_include)
    assert len(filtered) == 2
    filter_exclude = CategoryFilter(exclude=random.sample(cat_ids, 2))
    filtered = categories.filter(filter_exclude)
    assert len(filtered) == 2 # counting default wp category


    # Read
    cat = categories.get(cat.id)
    assert isinstance(cat, Category)

    # Update
    new_name = 'My new category name'
    cat = categories.update(cat.id, {'name': new_name})
    assert isinstance(cat, Category)
    assert cat.name == new_name

    # Delete
    for id in cat_ids:
        deleted = categories.delete(id)
        assert deleted == True

    filter = CategoryFilter()
    filter.include = cat_ids
    filtered = categories.filter(filter)
    assert len(filtered) == 0