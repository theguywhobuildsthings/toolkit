import time
from typing import Awaitable, Callable
from fastapi import WebSocket
import redis
import os
import threading
import json
import asyncio
import threading
import time
from typing import Awaitable, Callable
import redis
import os
import json
import asyncio
import logging

logger = logging.getLogger('output')

pool = redis.ConnectionPool(host=os.environ['REDIS_SERVER'], port=os.environ['REDIS_PORT'], db=0)

class RedisMessageThread(threading.Thread):
    id: str
    cb: Callable[[str], Awaitable[None]]

    def __init__(self, id: str, cb: Callable[[str], Awaitable[None]]):
        threading.Thread.__init__(self)
        self.cb = cb
        self.id = id
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        testy = redis.Redis()
        channel = testy.pubsub()
        channel.subscribe(self.id)
        while True:
            message = channel.get_message()
            if message and message is not None and isinstance(message, dict):
                logger.debug(f'Received message: { message } ')
                if message['type'] == 'message':
                    decoded_data = json.loads(message.get('data').decode("utf-8"))
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.cb(self, decoded_data))
                    loop.close()
            if self.stopped():
                logger.debug(f'Detected stop for thread {self.id}, dying')
                return
            time.sleep(0.1)

class ToolkitPubSub:
    async def send_message(self, id: str, message):
        testy = redis.Redis()
        testy.publish(id, json.dumps(message))
    
    def listen_for_message(self, id: str, cb: Callable[[str], Awaitable[None]]) -> RedisMessageThread:
        return RedisMessageThread(id, cb)


