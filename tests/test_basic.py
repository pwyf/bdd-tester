from os.path import abspath, dirname, join

import pytest

from bdd_tester import BDDTester
from bdd_tester.exceptions import UnknownStepException


EGGFUL_LIST = '''
SHOPPING LIST
=============

 * Bread
 * Butter
 * Milk
 * Eggs
'''


EGGLESS_LIST = '''
SHOPPING LIST
=============

 * Carrots
 * Tomatoes
 * Toothpaste
'''


EGG_LETTER = '''
Dear sir or madam,

I am writing to you about eggs.

Yours, Andy
'''


def test_succeeds():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    success, msg = feature.tests[0](EGGFUL_LIST, bdd_verbose=True)
    assert success is True
    assert msg is None

    success = feature.tests[0](EGGFUL_LIST)
    assert success is True


def test_not_relevant():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    success, msg = feature.tests[0](EGG_LETTER, bdd_verbose=True)
    assert success is None
    assert str(msg) == 'Not a shopping list'


def test_fails():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    success, msg = feature.tests[0](EGGLESS_LIST, bdd_verbose=True)
    assert success is False
    assert str(msg) == '"Eggs" not found'


def test_missing_step_definition():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    with pytest.raises(UnknownStepException):
        tester.load_feature(join(fixture_path, 'bad_feature.feature'))


def test_feature_repr():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    assert repr(feature) == '<Feature (Shopping list tests)>'


def test_tags_present():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    assert feature.tags[0] == 'feature-tag'
    test = feature.tests[0]
    assert test.tags[0] == 'test-tag'
    assert test.feature.tags[0] == 'feature-tag'
