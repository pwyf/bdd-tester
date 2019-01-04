from os.path import abspath, dirname, join

from bdd_tester import BDDTester


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
    assert msg == ''


def test_not_relevant():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    success, msg = feature.tests[0](EGG_LETTER, bdd_verbose=True)
    assert success is None
    assert msg == 'Not a shopping list'


def test_fails():
    fixture_path = join(dirname(abspath(__file__)), 'fixtures')

    tester = BDDTester(join(fixture_path, 'steps.py'))
    feature = tester.load_feature(join(fixture_path, 'feature.feature'))
    success, msg = feature.tests[0](EGGLESS_LIST, bdd_verbose=True)
    assert success is False
    assert msg == '"Eggs" not found'
