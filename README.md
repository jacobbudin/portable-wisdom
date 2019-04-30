# Portable Wisdom

Portable Wisdom is a tool to generate EPUB files from [Instapaper](https://www.instapaper.com/). You can then choose to sync these files to your ereader.

## Technologies

- Python 3

## Features

- Retrieves unread articles from Instapaper
- Embeds web images, downsizes them, and converts them to greyscale
- Caches articles and images
- Creates well-formatted EPUB files, tailored for your ereader

## Quick Start

1. Download and install Portable Wisdom from PyPI:

		$ pip install portable_wisdom

2. [Request an Instapaper API key.](https://www.instapaper.com/main/request_oauth_consumer_token) (Or copy one from a friend.)
4. Run Portable Wisdom from the command line:

		$ portable-wisdom --instapaper-key KEY \
			--instapaper-secret SECRET \
			--instapaper-login USER \
			--instapaper-password PASS

On success, the script will print the output filename. To view all of the options, run `$ portable-wisdom -h`.

## License

MIT License
