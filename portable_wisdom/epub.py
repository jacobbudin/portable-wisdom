from bs4 import BeautifulSoup
from ebooklib import epub
from . import transformers

def transform(book, function_names):
    """Apply transformation functions to ebook"""

    for item in book.items:
        if type(item) is not epub.EpubHtml:
            continue

        # Parse HTML
        soup = BeautifulSoup('<html><body>%s</body></html>' %
                             item.content, 'html5lib')

        # Apply transformations
        for name in function_names:
            function = getattr(transformers, name)
            function(book, soup)

        item.content = str(soup.body)
