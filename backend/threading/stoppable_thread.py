import threading
import time
from typing import Awaitable, Callable
import redis
import os
import json
import asyncio

class StoppableThread(threading.Thread):
    id: str
    cb: Callable[[str], Awaitable[None]]

    def __init__(self, id: str, cb: Callable[[str], Awaitable[None]]):
        threading.Thread.__init__(self)
        self.cb = cb
        self.id = id
        self._stop_event = threading.Event()
        print(f"Just made thread, stopped: {self.stopped()}")

    def stop(self):
        print("setting stop event")
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
                print(message.get('data') )
                if message['type'] == 'message':
                    decoded_data = json.loads(message.get('data').decode("utf-8"))
                    if decoded_data['message'] == 'pair-confirm':
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                        loop.run_until_complete(self.cb(decoded_data))
                        loop.close()
                    if 'exit_flow' in decoded_data and decoded_data['exit_flow'] == True:
                        return
            if self.stopped():
                print("Thread is dying")
                return
            time.sleep(0.1)