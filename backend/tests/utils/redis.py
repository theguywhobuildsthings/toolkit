from typing import Any


class RedisChannelMock:
    channel: str
    message: Any

    def __init__(self):
        self.channel = ""
        self.message = {}

    def subscribe(self, channel: str) -> None:
        self.channel = channel
    
    def get_message(self,) -> Any:
        m = self.message
        self.message = None
        return m

    def clear(self) -> None:
        self.channel = ""
        self.message = {}