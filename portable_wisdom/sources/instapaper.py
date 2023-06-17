import logging
from ..cache import cache
from ..article import Article
from ..config import INSTAPAPER_API_KEY, INSTAPAPER_API_SECRET, \
    INSTAPAPER_LOGIN, INSTAPAPER_PASSWORD, ARTICLE_LIMIT
from ..source import Source
from pyinstapaper.instapaper import Instapaper as PInstapaper


class Instapaper(Source):
    name = 'Instapaper'

    def get_articles(self):
        """Produce a list of Articles"""
        instapaper = PInstapaper(INSTAPAPER_API_KEY, INSTAPAPER_API_SECRET)

        try:
            instapaper.login(INSTAPAPER_LOGIN, INSTAPAPER_PASSWORD)
        except KeyError as e:
            if 'oauth_token' in str(e):
                logging.critical(
                    'Instapaper authentication failed; '
                    'check your API and user credentials')

            raise e

        # Enforce 25 article maximum
        limit = 25

        if ARTICLE_LIMIT:
            limit = min(limit, ARTICLE_LIMIT)

        bookmarks = instapaper.get_bookmarks('unread', limit)
        articles = []

        for bookmark in bookmarks:
            content = cache.get_or(bookmark.hash,
                                   lambda: bookmark.get_text()['data'].decode())  # noqa: E501
            article = Article(title=bookmark.title, content=content)
            articles.append(article)

        logging.info('Retrieved %d articles' % len(articles))
        return articles
