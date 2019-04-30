from bs4 import BeautifulSoup
from .cache import cache
from urllib.parse import urlparse
import os
from ebooklib import epub
import io
import logging
import requests
from PIL import Image
from .config import *

def embed_images(book):
    """Embeds remote images in EPUB HTML chapters"""
    image_names = set()

    for item in book.items:
        if type(item) is not epub.EpubHtml:
            continue
        
        # Parse HTML, find `img` elements
        soup = BeautifulSoup('<html><body>%s</body></html>' % item.content, 'html5lib')

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
                        content = requests.get(img['src']).content
                    except requests.exceptions.ContentDecodingError as e:
                        logging.error('Skipping image %s (%s)' % (img['src'], e))
                        continue
                    except requests.exceptions.ConnectionError as e:
                        logging.error('Skipping image %s (%s)' % (img['src'], e))
                        continue

                    original = io.BytesIO()
                    original.write(content)

                    try:
                        # Create smaller, greyscale image from source image
                        im = Image.open(original).convert('RGBA') # convert to `RGBA` before `L` or Pillow will complain
                        im.thumbnail(IMAGE_MAX_SIZE)
                        im = im.convert('L')
                        im.save(thumbnail, 'png' if ext == '.png' else 'jpeg')

                    except OSError as e:
                        logging.error('Skipping image %s (%s)' % (img['src'], e))
                        continue

                    cache.set(thumbnail_hash, thumbnail.getvalue())

                thumbnail.seek(0)

                image.content = thumbnail.read()
                book.add_item(image)
                image_names.add(name)

            img['style'] = 'max-width: 100%'
            img['src'] = name

        item.content = str(soup.body)
