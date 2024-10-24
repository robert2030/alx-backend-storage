#!/usr/bin/env python3
"""
File: exercise.py

Writing a string to Redis
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    parameters:
    - method (Callable): The method to be decorated

    Returns:
    - Callable: The decorated method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        count_key = key
        self._redis.incr(count_key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    parameters:
    - method (Callable): The method to be decorated

    Returns:
    - Callable: The decorated method
    """
    @wraps(method)
    def wrapper(self, *args):
        key = method.__qualname__
        inputs_key = key + ":inputs"
        outputs_key = key + ":outputs"

        # Log inputs
        self._redis.rpush(inputs_key, str(args))

        res = method(self, *args)

        # Log outputs
        self._redis.rpush(outputs_key, str(res))

        return res
    return wrapper


def replay(method: Callable):
    """
    parameters:
    - method (Callable): A method where a history of calls will
    be displayed.
    """
    redis_client = redis.Redis()
    inputs_key = method.__qualname__ + ":inputs"
    outputs_key = method.__qualname__ + ":outputs"

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    num_calls = len(inputs)

    print("{} was called {} times:".format(method.__qualname__, num_calls))
    for inp, out in zip(inputs, outputs):
        input_k = inp.decode("utf-8")
        output_k = out.decode("utf-8")
        print("{}(*{}) -> {}".format(method.__qualname__, input_k, output_k))


class Cache:
    """ Writing strings to Redis """
    def __init__(self):
        """
        Stores an instance of the Redis client as a private
        variable named _redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        parameters:
        - data (Union[str, bytes, int, float]): A value to the key.

        Returns:
        - (str): Returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) \
            -> Union[str, bytes, int, float]:
        """
        parameters:
        - key (str): The key used to retrieve data
        - fn (Collable): Optional collable, used to convert data back to the
        desired format.

        Returns:
        - Union[str, bytes, int, float]: The retrived data
        """
        data = self._redis.get(key)
        if data is None:
            return data
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, int, float]:
        """
        parameters:
        - key (str): The key used to retrieve data

        Returns:
        - Union[str, bytes, int, float]: The retrived data
        """
        return self.get(key, fu=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[str, bytes, int, float]:
        """
        parameters:
        - key (str): The key used to retrieve data

        Returns:
        - Union[str, bytes, int, float]: The retrived data
        """
        return self.get(key, fu=int)

