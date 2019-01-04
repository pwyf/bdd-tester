import re

from .core import Step


def given(pattern):
    return call(pattern)


def then(pattern):
    return call(pattern)


def call(pattern):
    def decorated(fn):
        Step.mappings.append((re.compile(r'^{}$'.format(pattern)), fn))
        return fn
    return decorated
