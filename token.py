class Token:
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __repr__(self):
        return 'Token{%s, %s}' % (self.value, self.tag)