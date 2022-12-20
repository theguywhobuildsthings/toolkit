from typing import Any
from unittest.mock import Mock


def make_coroutine(mock: Mock):
    async def coroutine(*args, **kwargs):
        return mock(*args, **kwargs)

    return coroutine


class RedisChannelMock:
    channel: str
    message: Any

    def __init__(self):
        self.channel = ""
        self.message = {}

    def subscribe(self, channel: str) -> None:
        self.channel = channel

    def get_message(
        self,
    ) -> Any:
        m = self.message
        self.message = None
        return m

    def clear(self) -> None:
        self.channel = ""
        self.message = {}


class RedisMessageThreadMock:
    def start():
        pass

    def stop():
        pass
