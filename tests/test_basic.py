from os.path import abspath, dirname, join

from bdd_tester import BDDTester


def test_core():
    steps_filepath = join(dirname(abspath(__file__)), 'fixtures', 'steps.py')
    tester = BDDTester(steps_filepath)
