#!/usr/bin/env python3
#
# Generate EPUB from Instapaper

import argparse
import datetime
from ebooklib import epub
import logging
from . import config
from .__version__ import __version__ as version
import sys
import os


def main():
    """Generate EPUB from Instapaper"""
    # Support CLI
    parser = argparse.ArgumentParser(
        description='Generate EPUB files from unread Instapaper articles')
    parser.add_argument(
        '--instapaper-api-key',
        help='Instapaper API key',
        default=os.environ.get('INSTAPAPER_API_KEY'))
    parser.add_argument(
        '--instapaper-api-secret',
        help='Instapaper API secret',
        default=os.environ.get('INSTAPAPER_API_SECRET'))
    parser.add_argument(
        '--instapaper-login',
        help='Instapaper account username or email address',
        default=os.environ.get('INSTAPAPER_LOGIN'))
    parser.add_argument(
        '--instapaper-password',
        help='Instapaper account password',
        default=os.environ.get('INSTAPAPER_PASSWORD'))
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
    parser.add_argument('-V', '--version', default=False,
                        action='store_true', help='print version number')

    args = parser.parse_args()

    if args.version:
        print(version)
        sys.exit(0)

    # Check for mandatory arguments
    mandatory_arguments = (
        'instapaper_api_key',
        'instapaper_api_secret',
        'instapaper_login',
        'instapaper_password')
    absent_arguments = []
    for arg in mandatory_arguments:
        try:
            value = getattr(args, arg)
            if value is None or len(value) == 0:
                raise AttributeError
        except AttributeError:
            absent_arguments.append(arg)

    if len(absent_arguments):
        logging.critical(
            'Instapaper credentials not provided: %s' %
            ', '.join(absent_arguments))
        sys.exit(1)

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
