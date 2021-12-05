import asyncio

from tests.fixtures import auth_data, media_data

from wpclient.client import Client
from wpclient.models.media import MediaModel


async def create(auth_data, media_data):
    async with Client(**auth_data) as client:
        media = MediaModel.parse_obj(media_data)
        coro = client.media.create(media)
        client.add(coro)
        await client.perform()
        return client.result

async def get(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.media.get(id)
        client.add(coro)
        await client.perform()
        return client.result

async def update(auth_data, id, media_updated):
    async with Client(**auth_data) as client:
        coro = client.media.update(id, media_updated)
        client.add(coro)
        await client.perform()
        return client.result


async def delete(auth_data, id):
    async with Client(**auth_data) as client:
        coro = client.media.delete(id)
        client.add(coro)
        await client.perform()
        return client.result


def test_async_crud(auth_data, media_data):
    r = asyncio.run(create(auth_data, media_data))
    media = r[0]
    assert isinstance(media, MediaModel)
    r = asyncio.run(get(auth_data, media.id))
    media = r[0]
    assert media.alt_text == media_data['alt_text']
    media_updated = media_data.copy()
    media_updated['alt_text'] = 'My updated alt text'
    r = asyncio.run(update(auth_data, media.id, media_updated))
    media = r[0]
    assert media.alt_text == media_updated['alt_text']
    r = asyncio.run(delete(auth_data, media.id))
    assert r[0] == True

