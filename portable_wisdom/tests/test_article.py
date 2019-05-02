from unittest import TestCase
from portable_wisdom.article import Article

title = 'Bank Robber Strikes Again'
content = '$1m was stolen from First Federal Bank yesterday.'


class TestArticle(TestCase):
    def test_init(self):
        a = Article(title, content)
        self.assertEqual(a.title, title)
        self.assertEqual(a.content, content)

    def test_str(self):
        a = Article(title, content)
        self.assertIn(title, str(a))
        self.assertNotIn(content, str(a))
