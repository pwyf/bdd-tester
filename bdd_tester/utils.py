import re


store = {}


def given(pattern):
    return call(pattern)


def then(pattern):
    return call(pattern)


def call(pattern):
    def decorated(fn):
        store[pattern] = ((re.compile(r'^{}$'.format(pattern)), fn))
        return fn
    return decorated
