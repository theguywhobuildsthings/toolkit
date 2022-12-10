from typing import Awaitable, Callable
import redis
import os
import threading
import json
import asyncio

pool = redis.ConnectionPool(host=os.environ['REDIS_SERVER'], port=os.environ['REDIS_PORT'], db=0)

class ToolkitPubSub:
    async def send_message(self, id: str, message):
        testy = redis.Redis()
        testy.publish(id, json.dumps(message))
    
    def listen_for_message(self, id: str, cb: Callable[[str], Awaitable[None]]):
        threading.Thread(target=self.__start_listening, args=[id, cb]).start()
        
    def __start_listening(self, id: str, cb: Callable[[str], Awaitable[None]]):
        testy = redis.Redis()
        channel = testy.pubsub()
        channel.subscribe(id)
        for message in channel.listen():
            print(f'received: {str(message)}')
            if message is not None and isinstance(message, dict):
                print(message.get('data') )
                if message['type'] == 'message':
                    decoded_data = json.loads(message.get('data').decode("utf-8"))
                    if decoded_data['message'] == 'pair-confirm':
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                        loop.run_until_complete(cb(decoded_data))
                        loop.close()
                    if 'exit_flow' in decoded_data and decoded_data['exit_flow'] == True:
                        return
                

    
