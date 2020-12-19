class Token:
    def __init__(self, value, classification):
        self.value = value
        self.classification = classification

    def __repr__(self):
        return 'Token{%s, %s}' % (self.value, self.classification)