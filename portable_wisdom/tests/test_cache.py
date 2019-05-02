from unittest import TestCase
from random import choice
from portable_wisdom.cache import Cache


class TestCache(TestCase):
    def test_get(self):
        c = Cache()
        v = choice(range(1, 255))
        c.set('some_key', v)
        self.assertEqual(c.get('some_key'), v)
        c.clear()

    def test_get_empty(self):
        c = Cache()
        self.assertIsNone(c.get('some_absent_key'))
        c.clear()

    def test_get_or(self):
        c = Cache()
        v = choice(range(1, 255))
        print(v)
        c.get_or('some_key', lambda: v)
        self.assertEqual(c.get('some_key'), v)
        c.clear()

    def test_get_or2(self):
        c = Cache()
        v = choice(range(1, 255))
        c.set('some_key', v)
        c.get_or('some_key', lambda: v+1)
        self.assertEqual(c.get('some_key'), v)
        c.clear()

    def test_set(self):
        c = Cache()
        v = choice(range(1, 255))
        c.set('some_key', v)
        self.assertEqual(c.get('some_key'), v)
        c.clear()
