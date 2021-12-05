import asyncio

from tests.fixtures import auth_data, category_data

from wpclient.client import Client
from wpclient.models.category import Category


async def create(auth_data, category_data):
    async with Client(**auth_data) as client:
        category = Category.parse_obj(category_data)
        coro = client.categories.create(category)
        client.add(coro)
        await client.perform()
        return client.result

async def get(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.categories.get(id)
        client.add(coro)
        await client.perform()
        return client.result

async def update(auth_data, id, category_updated):
    async with Client(**auth_data) as client:
        coro = client.categories.update(id, category_updated)
        client.add(coro)
        await client.perform()
        return client.result


async def delete(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.categories.delete(id)
        client.add(coro)
        await client.perform()
        return client.result


def test_async_crud(auth_data, category_data):
    r = asyncio.run(create(auth_data, category_data))
    category = r[0]
    assert isinstance(category, Category)
    r = asyncio.run(get(auth_data, category.id))
    category = r[0]
    assert category.name == category_data['name']
    category_updated = category_data.copy()
    category_updated['name'] = 'My updated title'
    r = asyncio.run(update(auth_data, category.id, category_updated))
    category = r[0]
    assert category.name == category_updated['name']
    r = asyncio.run(delete(auth_data, category.id))
    assert r[0] == True

