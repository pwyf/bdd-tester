import re


store = {}


def given(pattern, loop=False):
    return call(pattern, loop)


def then(pattern, loop=False):
    return call(pattern, loop)


def call(pattern, loop=False):
    def decorated(fn):
        store[pattern] = (re.compile(r'^{}$'.format(pattern)), fn, loop)
        return fn  # this isn't needed, but useful for testing
    return decorated
