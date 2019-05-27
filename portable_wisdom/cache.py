from .config import CACHE_SIZE
from diskcache import Cache as DiskCache
import logging
import os

CACHE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp')


class Cache:
    def __init__(self):
        self.cache = DiskCache(CACHE_PATH, size_limit=CACHE_SIZE)

    def get(self, key):
        value = self.cache.get(key)

        if value:
            logging.debug('Hit cache key %s' % key)

        return value

    def clear(self):
        return self.cache.clear()

    def set(self, key, value):
        return self.cache.set(key, value)

    def get_or(self, key, _or):
        """Get a key's value, or use function's return value to set"""
        if key in self.cache:
            logging.debug('Hit cache key %s' % key)
            return self.cache[key]

        value = _or()
        self.cache.set(key, value)
        return value


cache = Cache()
