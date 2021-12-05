import asyncio

from tests.fixtures import auth_data, tag_data

from wpclient.client import Client
from wpclient.models.tag import Tag


async def create(auth_data, tag_data):
    async with Client(**auth_data) as client:
        tag = Tag.parse_obj(tag_data)
        coro = client.tags.create(tag)
        client.add(coro)
        await client.perform()
        return client.result

async def get(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.tags.get(id)
        client.add(coro)
        await client.perform()
        return client.result

async def update(auth_data, id, tag_updated):
    async with Client(**auth_data) as client:
        coro = client.tags.update(id, tag_updated)
        client.add(coro)
        await client.perform()
        return client.result


async def delete(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.tags.delete(id)
        client.add(coro)
        await client.perform()
        return client.result


def test_async_crud(auth_data, tag_data):
    r = asyncio.run(create(auth_data, tag_data))
    tag = r[0]
    assert isinstance(tag, Tag)
    r = asyncio.run(get(auth_data, tag.id))
    tag = r[0]
    assert tag.name == tag_data['name']
    tag_updated = tag_data.copy()
    tag_updated['name'] = 'My updated title'
    r = asyncio.run(update(auth_data, tag.id, tag_updated))
    tag = r[0]
    assert tag.name == tag_updated['name']
    r = asyncio.run(delete(auth_data, tag.id))
    assert r[0] == True

