from dishka import Provider, Scope, provide

from workBirthdays.core.utils.lock_factory import LockFactory, MemoryLockFactory


class LockProvider(Provider):
    scope = Scope.APP

    @provide
    def get_lock_factory(self) -> LockFactory:
        return MemoryLockFactory()
