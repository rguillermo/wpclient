import asyncio

from tests.fixtures import auth_data, post_data

from wpclient.client import Client
from wpclient.models.post import Post


async def create(auth_data, post_data):
    async with Client(**auth_data) as client:
        post = Post.parse_obj(post_data)
        coro = client.posts.create(post)
        client.add(coro)
        await client.perform()
        return client.result

async def get(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.posts.get(id)
        client.add(coro)
        await client.perform()
        return client.result

async def update(auth_data, id, post_updated):
    async with Client(**auth_data) as client:
        coro = client.posts.update(id, post_updated)
        client.add(coro)
        await client.perform()
        return client.result


async def delete(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.posts.delete(id)
        client.add(coro)
        await client.perform()
        return client.result


def test_async_crud(auth_data, post_data):
    r = asyncio.run(create(auth_data, post_data))
    post = r[0]
    assert isinstance(post, Post)
    r = asyncio.run(get(auth_data, post.id))
    post = r[0]
    assert post.title == post_data['title']
    post_updated = post_data.copy()
    post_updated['title'] = 'My updated title'
    r = asyncio.run(update(auth_data, post.id, post_updated))
    post = r[0]
    assert post.title == post_updated['title']
    r = asyncio.run(delete(auth_data, post.id))
    assert r[0] == True

