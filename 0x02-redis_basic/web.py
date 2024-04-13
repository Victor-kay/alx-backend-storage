#!/usr/bin/env python3
"""
web.py: Implements a function to fetch web pages and caches them with a counter and expiration time.
"""

import requests
import time
import functools
import redis

CACHE = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_decorator(func):
    """
    Decorator to cache function results with expiration time.
    """
    @functools.wraps(func)
    def wrapper(url: str) -> str:
        key = f"count:{url}"
        count = CACHE.get(key)
        
        if count:
            CACHE.incr(key)
            return CACHE.get(url).decode('utf-8')

        content = func(url)
        CACHE.setex(url, 10, content)
        CACHE.set(key, 1, ex=10)
        return content

    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and returns it.
    
    Args:
    - url (str): The URL to fetch.
    
    Returns:
    - str: The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text


if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    
    for _ in range(5):
        print(get_page(url))
        time.sleep(2)
