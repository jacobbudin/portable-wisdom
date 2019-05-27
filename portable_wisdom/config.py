# HTML elements that are preserved
ALLOWED_TAGS = ('p', 'b', 'i', 'blockquote', 'strong',
                'em', 'figure', 'figcaption', 'img')

# HTML element attributes that are preserved
ALLOWED_ATTRIBUTES = ('src', )

# Default transformers to apply
TRANSFORM = (
    'remove_duplicative_blockquotes',
    'embed_images',
    'strip_links',
    'beautify_hr'
)

# Instapaper configuration
INSTAPAPER_KEY = ''
INSTAPAPER_SECRET = ''
INSTAPAPER_LOGIN = ''
INSTAPAPER_PASSWORD = ''

# Maximum number of articles to include
ARTICLE_LIMIT = 25

# Maximum dimensions of embedded images
IMAGE_MAX_SIZE = (600, 600)

# Output filename
OUTPUT = None

# Name of stylesheet to use
STYLE = 'nook-glowlight-3'

# Quiet mode
QUIET = False

# Debug mode
DEBUG = False

# Verbose mode
VERBOSE = False
