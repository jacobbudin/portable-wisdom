from ebooklib import epub
from unittest import TestCase
from portable_wisdom.source import Source
from portable_wisdom.article import Article

articles = (
        Article('Bank Robber Strikes Again',
                '$1m was stolen from First Federal Bank yesterday.'),
        Article('UFO Lands in Area 51',
                'Aliens greeted humans with peace sign.'),
    )


class FakeSource(Source):
    name = 'Lies Magazine'

    def get_articles(self):
        return articles


class TestSource(TestCase):
    def test_to_epub(self):
        source = FakeSource()
        book = source.to_epub()

        chapters = 0
        for item in book.items:
            if type(item) is epub.EpubHtml:
                chapters += 1

        self.assertEqual(len(articles), chapters)
