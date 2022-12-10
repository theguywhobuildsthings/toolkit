import time
from typing import Awaitable, Callable
import redis
import os
import threading
import json
import asyncio

from backend.threading.stoppable_thread import StoppableThread

pool = redis.ConnectionPool(host=os.environ['REDIS_SERVER'], port=os.environ['REDIS_PORT'], db=0)

class ToolkitPubSub:
    async def send_message(self, id: str, message):
        testy = redis.Redis()
        testy.publish(id, json.dumps(message))
    
    def listen_for_message(self, id: str, cb: Callable[[str], Awaitable[None]]) -> StoppableThread:
        return StoppableThread(id, cb)
        
        
            
                

    
