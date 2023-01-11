#!/usr/bin/env python3
#
# Generate EPUB from Instapaper

import argparse
import datetime
from ebooklib import epub
import logging
from . import config
import sys


def main():
    """Generate EPUB from Instapaper"""
    # Support CLI
    parser = argparse.ArgumentParser(
        description='Generate EPUB from Instapaper')
    parser.add_argument('--instapaper-key', help='Instapaper API key')
    parser.add_argument('--instapaper-secret', help='Instapaper API secret')
    parser.add_argument('--instapaper-login',
                        help='Instapaper account username or email address')
    parser.add_argument('--instapaper-password',
                        help='Instapaper account password')
    parser.add_argument('-o', '--output', default=config.OUTPUT,
                        metavar='FILE', help='output filename')
    parser.add_argument('-s', '--style', default=config.STYLE,
                        metavar='PRESET|FILE', help='stylesheet to use')
    parser.add_argument('-t', '--transform', default=config.TRANSFORM,
                        nargs='+', metavar='FUNCTION',
                        help='transformer functions')
    parser.add_argument('-l', '--article-limit', '--limit',
                        default=config.ARTICLE_LIMIT, metavar='LIMIT',
                        type=int, help='number of articles to include')
    parser.add_argument('-q', '--quiet', default=False,
                        action='store_true',
                        help='do not print standard output')
    parser.add_argument('-v', '--verbose', default=False,
                        action='store_true', help='verbose mode')
    parser.add_argument('-d', '--debug', default=False,
                        action='store_true', help='debug mode')

    args = parser.parse_args()

    # Where an option is provided, override its configuration value
    for option, value in vars(args).items():
        if value:
            setattr(config, option.upper(), value)

    logging_level = logging.CRITICAL
    if config.VERBOSE or config.DEBUG:
        logging_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging_level)

    # Check for multiple output options
    output_options = (config.QUIET, config.VERBOSE, config.DEBUG)
    if len(tuple(filter(lambda x: x is True, output_options))) > 1:
        logging.critical('Cannot use multiple output flags')
        sys.exit(1)

    # Import after configuration is set
    from .epub import transform
    from .sources.instapaper import Instapaper

    # Create EPUB and save to disk
    source = Instapaper
    book = source().to_epub()
    transform(book, config.TRANSFORM)

    filename = config.OUTPUT
    if not filename:
        today = datetime.datetime.today()
        filename = '{} - {:%Y-%m-%d}.epub'.format(source.name, today)

    epub.write_epub(filename, book, {})
    if not config.QUIET:
        print(filename)


if __name__ == '__main__':
    main()
