from .cache import cache
from urllib.parse import urlparse
import os
from ebooklib import epub
import io
import logging
import re
import requests
from PIL import Image
from .config import IMAGE_GREYSCALE, IMAGE_MAX_SIZE

hr_like = re.compile(r"""^[\*\-—~ ]+$""")


def beautify_hr(book, soup):
    """Replaces rule-like elements with `hr`"""

    for el in soup.find_all('p'):
        content = el.string

        if not content:
            continue

        if re.match(hr_like, content.strip()):
            el.insert_before(soup.new_tag('hr'))
            el.decompose()

    # Replace back-to-back `hr`s
    for el in soup.find_all('hr'):
        previous = el.previous_sibling
        if previous and previous.name == 'hr':
            previous.decompose()

    # Never begin or end with `hr`
    if len(soup.body.contents):
        first = soup.contents[0]
        last = soup.contents[-1]

        if first.name == 'hr':
            first.decompose()

        if last.name == 'hr':
            last.decompose()


def remove_duplicative_blockquotes(book, soup):
    """Removes `blockquote` elements that contain duplicated copy"""

    # Create a string with all article text in `p`s
    copy = ""
    for p in soup.find_all('p'):
        if p.string:
            copy += p.string

    # Iterate over `blockquotes`, removing those with text from article text
    for blockquote in soup.find_all('blockquote'):
        quote = blockquote.string

        if not quote:
            continue

        quote = quote.strip()
        if quote in copy:
            logging.debug('Removing blockquote: %s', quote)
            blockquote.decompose()


def strip_links(book, soup):
    """Replaces `a` elements with `span.link`"""

    for a in soup.find_all('a'):
        a.name = 'span'
        a['class'] = 'link'


image_names = set()


def embed_images(book, soup):
    """Embeds remote images in EPUB HTML chapters"""

    for img in soup.find_all('img'):
        src = img.get('src')

        # Remove junk images
        if not src:
            img.decompose()
            continue
        if src.startswith('denied:'):
            img.decompose()
            continue
        if src.startswith('data:'):
            img.decompose()
            continue

        src_parts = urlparse(src)
        ext = os.path.splitext(src_parts.path)[1]
        name = str(hash(src)) + ext

        if name not in image_names:
            # Create `EpubImage` wrapper object
            image = epub.EpubImage()
            image.id = str(hash(src))
            image.file_name = name

            thumbnail_hash = src + str(IMAGE_MAX_SIZE)
            thumbnail_bytes = cache.get(thumbnail_hash)

            # Download the image
            if thumbnail_bytes:
                thumbnail = io.BytesIO(thumbnail_bytes)
            else:
                thumbnail = io.BytesIO()

                try:
                    logging.info('Downloading image %s', img['src'])
                    content = requests.get(img['src'], timeout=3.05).content
                except (requests.exceptions.ContentDecodingError,
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.InvalidSchema) as e:
                    logging.error('Skipping image %s (%s)' %
                                  (img['src'], e))
                    continue

                original = io.BytesIO()
                original.write(content)

                try:
                    # Create smaller, greyscale image from source image
                    # convert to `RGBA` before `L` or Pillow will complain
                    im = Image.open(original).convert('RGBA')
                    im.thumbnail(IMAGE_MAX_SIZE)
                    if IMAGE_GREYSCALE:
                        im = im.convert('L')
                    im.save(thumbnail, 'png' if ext == '.png' else 'jpeg')

                except OSError as e:
                    logging.error('Skipping image %s (%s)' %
                                  (img['src'], e))
                    continue

                cache.set(thumbnail_hash, thumbnail.getvalue())

            thumbnail.seek(0)

            image.content = thumbnail.read()
            book.add_item(image)
            image_names.add(name)

        img['style'] = 'max-width: 100%'
        img['src'] = name
