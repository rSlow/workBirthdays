import asyncio
from typing import Protocol


class KeyCheckerLock(Protocol):
    async def acquire(self):
        raise NotImplementedError

    async def release(self):
        raise NotImplementedError

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()


class LockFactory(Protocol):  # TODO check usages
    def lock_globally(self) -> KeyCheckerLock:
        raise NotImplementedError

    def __call__(self) -> KeyCheckerLock:
        return self.lock_globally()

    def clear(self) -> None:
        raise NotImplementedError


class MemoryLock(KeyCheckerLock):
    def __init__(self) -> None:
        self.lock = asyncio.Lock()

    async def acquire(self):
        await self.lock.acquire()

    async def release(self):
        self.lock.release()


class MemoryLockFactory(LockFactory):
    def __init__(self) -> None:
        self.global_lock = MemoryLock()

    def lock_globally(self) -> KeyCheckerLock:
        return self.global_lock

    def clear(self):
        pass
