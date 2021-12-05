import asyncio
from collections.abc import Coroutine
from typing import Any, Optional


class Manager:
    def __init__(self, semaphore_value=100):
        self.sempahore = asyncio.Semaphore(semaphore_value)
        self.tasks: list[Coroutine] = []
        self.result: Optional[Any] = None
        self.loop = asyncio.new_event_loop()

    def add(self, coro: Coroutine):
        self.tasks.append(self.loop.create_task(coro))

    async def perform(self):
        self.result = await asyncio.gather(*self.tasks)

    def run(self):
        self.loop.run_until_complete(self.perform())
