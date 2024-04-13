#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data in Redis.
"""

import redis
import uuid
import functools
from typing import Callable, Union

class Cache:
    """
    Cache class for storing and retrieving data in Redis.
    """

    def __init__(self):
        """
        Initialize the Cache class with a Redis instance.
        """
        self._redis = redis.Redis()

    def clear_cache(self):
        """
        Clear all data from the Redis cache.
        """
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis and return the generated key.
        
        Args:
            data (Union[str, bytes, int, float]): The data to store.
        
        Returns:
            str: The generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int]:
        """
        Retrieve data from Redis using the given key.
        
        Args:
            key (str): The key to retrieve data.
            fn (Callable, optional): Callable function to convert the retrieved data.
        
        Returns:
            Union[str, bytes, int]: The retrieved data.
        """
        value = self._redis.get(key)
        if value is None:
            return value

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve and decode a string value from Redis using the given key.
        
        Args:
            key (str): The key to retrieve data.
        
        Returns:
            str: The decoded string value.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve and convert an integer value from Redis using the given key.
        
        Args:
            key (str): The key to retrieve data.
        
        Returns:
            int: The converted integer value.
        """
        return self.get(key, fn=int)

    def count_calls(method):
        """
        Decorator to count the number of calls to a method.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis, count the call, and return the generated key.
        
        Args:
            data (Union[str, bytes, int, float]): The data to store.
        
        Returns:
            str: The generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def call_history(method):
        """
        Decorator to store call history of a method.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = f"{method.__qualname__}:inputs"
            outputs_key = f"{method.__qualname__}:outputs"
            
            self._redis.rpush(inputs_key, str(args))
            
            result = method(self, *args, **kwargs)
            
            self._redis.rpush(outputs_key, result)
            
            return result
        return wrapper

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis, store the call history, and return the generated key.
        
        Args:
            data (Union[str, bytes, int, float]): The data to store.
        
        Returns:
            str: The generated key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

class WebCache:
    """
    WebCache class for caching web pages with expiration and tracking access count.
    """

    def __init__(self):
        """
        Initialize the WebCache class with a Redis instance.
        """
        self._redis = redis.Redis()

    def get_page(self, url: str) -> str:
        """
        Retrieve the HTML content of a web page.
        
        Args:
            url (str): The URL of the web page.
        
        Returns:
            str: The HTML content of the web page.
        """
        count_key = f"count:{url}"
        content_key = f"content:{url}"
        
        # Increment count
        self._redis.incr(count_key)
        
        # Check cache
        cached_content = self._redis.get(content_key)
        if cached_content:
            return cached_content.decode("utf-8")
        
        # Fetch content
        response = requests.get(url)
        content = response.text
        
        # Cache content with expiration
        self._redis.setex(content_key, 10, content)
        
        return content
