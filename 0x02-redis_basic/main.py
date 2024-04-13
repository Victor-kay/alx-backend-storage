#!/usr/bin/env python3
"""
Main file
"""
import redis

class Cache:
    def __init__(self):
        self._redis = redis.Redis()

    def store(self, data):
        key = self._generate_key(data)
        self._redis.set(key, data)
        return key

    def get(self, key):
        return self._redis.get(key)

    def _generate_key(self, data):
        return str(hash(data))

if __name__ == "__main__":
    cache = Cache()

    # First main file
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))

    # Second main file
    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))

    # Third main file
    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
