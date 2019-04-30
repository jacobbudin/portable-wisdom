class Article:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return 'Article("%s", "%s")' % (self.title, self.content)

    def __str__(self):
        return '"%s"' % self.title
