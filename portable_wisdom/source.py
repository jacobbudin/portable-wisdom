import os.path
from .config import STYLE
from ebooklib import epub
import logging

STYLES_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'styles')


class Source:
    def to_epub(self, style=None):
        """Generate `EpubBook` from result of `get_articles`"""
        if not style:
            style = STYLE

        logging.info('Creating book using %s style' % style)
        articles = self.get_articles()

        book = epub.EpubBook()
        book.set_title(self.__class__.name)

        # Create HTML file for each article
        chapters = []
        for i, article in enumerate(articles):
            chapter = epub.EpubHtml(
                uid=str(i), title=article.title, file_name=('%d.xhtml' % i))
            chapter.content = '<html><head>' + \
                '<link rel="stylesheet" href="style/default.css" />' + \
                '</head><body>' + \
                ('<h1>%s</h1>' % article.title) + \
                article.content + '</body></html>'
            chapters.append(chapter)
            book.add_item(chapter)

        # Add generic book metadata
        book.toc = map(lambda c: epub.Link(
            c.get_name(), c.title, str(c.get_id())), chapters)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Add stylesheet
        # Use path if file exists
        if os.path.exists(style):
            style_path = style
            logging.debug('Using custom style %s' % style)
        # Otherwise use preset style
        else:
            style_name = style if style.endswith('.css') else style + '.css'
            style_path = os.path.join(STYLES_PATH, style_name)

            if not os.path.exists(style_path):
                raise Exception('%s is not a preset style' % style)

            logging.debug('Using preset style %s' % style)

        with open(style_path) as f:
            nav_css = epub.EpubItem(
                uid="style_nav", file_name="style/default.css",
                media_type="text/css", content=f.read())

        book.add_item(nav_css)

        book.spine = ['nav'] + chapters

        return book
