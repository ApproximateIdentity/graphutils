class Pairwise(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self

    def next(self):
        a = self.iterable.next()
        b = self.iterable.next()
        return (a, b)

