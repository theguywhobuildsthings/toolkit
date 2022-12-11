import asyncio
import json
import time
from unittest import TestCase
from unittest.mock import MagicMock, Mock
import pytest
import redis

from backend.redis.redis import RedisMessageThread
from backend.tests.utils.redis import RedisChannelMock

mock_redis = redis.Redis()
mock_redis_channel = RedisChannelMock()

def test_correct_channel_subscription():
    mock_redis.pubsub = MagicMock(return_value=mock_redis_channel)
    channel_name = "test"
    thread = RedisMessageThread(channel_name, lambda x: print(x), mock_redis)
    thread.start()
    thread.stop()
    assert mock_redis_channel.channel == channel_name, "Correct channel should be subscribed to "
    mock_redis_channel.clear()

def test_incorrect_channel_subscription():
    mock_redis.pubsub = MagicMock(return_value=mock_redis_channel)
    channel_name = "test"
    thread = RedisMessageThread("not_test", lambda x: print(x), mock_redis)
    thread.start()
    thread.stop()
    assert mock_redis_channel.channel != channel_name, "Correct channel should be subscribed to "
    mock_redis_channel.clear()


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
     
def test_callback_receives_correct_message():
    mock_redis.pubsub = MagicMock(return_value=mock_redis_channel)
    channel_name = "test"
    expected_output = {'hey': 'there'}
    mock_redis_channel.message = {'type': 'message', 'data': bytes(json.dumps(expected_output), 'utf-8')}
    # out_thread, out_message = None, None
    # passed = False
    # print(out_message)
    cb = Mock()
    # async def set_output_values(x, y):
    #     TestCase().assertDictEqual(expected_output, y)
        
    #     passed = True
    d = asyncio.Future()
    d.set_result("te")
    thread = RedisMessageThread(channel_name, d, mock_redis)
    thread.start()
    time.sleep(0.5)
    thread.stop()
    # cb.assert_called()
    # assert passed, 'expected callback to be fired within 1 second'
    # print(out_message)
    
    # assert out_message == expected_output, "Correct information should be passed into callback"
    # mock_redis_channel.clear()