import json
import time
from unittest.mock import MagicMock, Mock
import redis
from unittest.mock import ANY

from backend.redis.redis import RedisMessageThread
from backend.tests.utils.redis import RedisChannelMock, make_coroutine

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
     
def test_callback_receives_correct_message():
    mock_redis.pubsub = MagicMock(return_value=mock_redis_channel)
    channel_name = "test"
    expected_output = {'hey': 'there'}
    mock_redis_channel.message = {'type': 'message', 'data': bytes(json.dumps(expected_output), 'utf-8')}
    cb = Mock()
    coroutine = make_coroutine(cb)

    thread = RedisMessageThread(channel_name, coroutine, mock_redis)
    thread.start()
    time.sleep(0.1)
    thread.stop()

    cb.assert_called_once_with(ANY, expected_output)

def test_subscription_message_not_passed():
    mock_redis.pubsub = MagicMock(return_value=mock_redis_channel)
    channel_name = "test"
    expected_output = {'hey': 'there'}
    mock_redis_channel.message = {'type': 'subscription', 'data': bytes(json.dumps(expected_output), 'utf-8')}
    cb = Mock()
    coroutine = make_coroutine(cb)

    thread = RedisMessageThread(channel_name, coroutine, mock_redis)
    thread.start()
    time.sleep(0.1)
    thread.stop()

    cb.assert_not_called()