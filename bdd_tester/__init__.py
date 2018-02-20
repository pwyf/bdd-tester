from .utils import given, then
from .exceptions import StepException


def bdd_tester(stepfile_filepath):
    from .core import BDDTester
    return BDDTester(stepfile_filepath)
