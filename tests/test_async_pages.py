import asyncio

from tests.fixtures import auth_data, page_data

from wpclient.client import Client
from wpclient.models.page import Page


async def create(auth_data, page_data):
    async with Client(**auth_data) as client:
        page = Page.parse_obj(page_data)
        coro = client.posts.create(page)
        client.add(coro)
        await client.perform()
        return client.result

async def get(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.posts.get(id)
        client.add(coro)
        await client.perform()
        return client.result

async def update(auth_data, id, page_updated):
    async with Client(**auth_data) as client:
        coro = client.posts.update(id, page_updated)
        client.add(coro)
        await client.perform()
        return client.result


async def delete(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.posts.delete(id)
        client.add(coro)
        await client.perform()
        return client.result


def test_async_crud(auth_data, page_data):
    r = asyncio.run(create(auth_data, page_data))
    page = r[0]
    assert isinstance(page, Page)
    r = asyncio.run(get(auth_data, page.id))
    page = r[0]
    assert page.title == page_data['title']
    page_updated = page_data.copy()
    page_updated['title'] = 'My updated title'
    r = asyncio.run(update(auth_data, page.id, page_updated))
    page = r[0]
    assert page.title == page_updated['title']
    r = asyncio.run(delete(auth_data, page.id))
    assert r[0] == True

