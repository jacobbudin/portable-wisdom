#!/usr/bin/env python3
#
# Generate EPUB from Instapaper

import argparse
import datetime
from ebooklib import epub
import logging
from . import config

def main():
    """Generate EPUB from Instapaper"""
    # Support CLI
    parser = argparse.ArgumentParser(description='Generate EPUB from Instapaper')
    parser.add_argument('--instapaper-key', help='Instapaper API key')
    parser.add_argument('--instapaper-secret', help='Instapaper API secret')
    parser.add_argument('--instapaper-login', help='Instapaper account username or email address')
    parser.add_argument('--instapaper-password', help='Instapaper account password')
    parser.add_argument('-s', '--style', default=config.STYLE, help='stylesheet to use')
    parser.add_argument('-l', '--article-limit', '--limit', default=config.ARTICLE_LIMIT, metavar='LIMIT', type=int, help='number of articles to include')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='verbose mode')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='debug mode')

    args = parser.parse_args()

    # Where an option is provided, override its configuration value
    for option, value in vars(args).items():
        if value:
            setattr(config, option.upper(), value)

    logging_level = logging.CRITICAL
    if config.VERBOSE or config.DEBUG:
        logging_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging_level)

    # Import after configuration is set
    from .epub import embed_images
    from .sources import Instapaper

    # Create EPUB and save to disk
    source = Instapaper
    book = source().to_epub()
    embed_images(book)

    today = datetime.datetime.today()
    filename = '%s - %s-%s-%s.epub' % (source.name, today.year, today.month, today.day)
    epub.write_epub(filename, book, {})
    print(filename)

if __name__ == '__main__':
    main()
