# Portable Wisdom

Portable Wisdom is a command-line tool to generate EPUB files from your recent unread articles in [Instapaper](https://www.instapaper.com/). You can then copy these files to your ereader.

## Technologies

- Python 3

## Features

- Retrieves unread articles from Instapaper
- Finds and downloads images from the web, downsizes them, converts them to greyscale, and embeds them into the file
- Caches articles and images, runs fast for heavy users
- Creates well-formatted EPUB files tailored for your ereader

## Quick Start

1. Download and install Portable Wisdom from PyPI:

		$ pip install portable-wisdom

2. [Request an Instapaper API key.](https://www.instapaper.com/main/request_oauth_consumer_token) (Or copy one from a friend.)
4. Run Portable Wisdom from the command line:

		$ portable-wisdom --instapaper-key KEY \
			--instapaper-secret SECRET \
			--instapaper-login USER \
			--instapaper-password PASS

On success, the script will print the output filename. To view all of the options, run `$ portable-wisdom -h`.

## Compatibility

Portable Wisdom uses [`EbookLib`](https://pypi.org/project/EbookLib/) to create EPUB files. These files are compatible with most ereaders—including Nook, Kobo, and Sony—as well as most ebook software. Kindle owners can use [Pandoc](https://pandoc.org/) or a similar tool to convert from EPUB to MOBI.

### Styles

Portable Wisdom supports styles (`--style`) to create EPUB files optimized for your ereader's rendering engine. These styles are regular CSS files. They specify header sizes, image layout, quote formatting, etc. Use the default style or create your own.

## Contributing

To report a bug or request a feaure, [create an issue on GitHub](https://github.com/jacobbudin/portable-wisdom/issues/new). Developers are welcome and encouraged to submit pull requests, but contributors should strongly consider creating an issue and requesting comments before starting work.

### Guidelines

- Comply with [PEP 8](https://www.python.org/dev/peps/pep-0008/) (use [Flake8](https://pypi.org/project/flake8/) to confirm)
- Run and pass all tests
	- Create new tests or refine existing ones, if necessary

## License

MIT License
