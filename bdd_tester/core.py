from gherkin.parser import Parser as GherkinParser
import six

from .exceptions import StepException, UnknownStepException
from . import utils

if six.PY3:
    from importlib import reload
    from importlib.machinery import SourceFileLoader
else:
    from imp import load_source, reload


class Feature:
    def __init__(self, feature_dict, tester):
        self.tester = tester

        self.name = feature_dict['name']
        self.tags = [tag['name'][1:] for tag in feature_dict['tags']]

        self.tests = [Test(test_dict, self)
                      for test_dict in feature_dict['children']]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, str(self))


class Test:
    def __init__(self, test_dict, feature):
        self.feature = feature

        self.name = test_dict['name']
        self.tags = [tag['name'][1:] for tag in test_dict['tags']]

        self.steps = []
        step_type = 'given'
        for step_dict in test_dict['steps']:
            if step_dict['keyword'].lower().strip() == 'then':
                step_type = 'then'
            self.steps.append(Step(step_dict, step_type, self))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, str(self))

    def loop(self, obj, steps, *args, **kwargs):
        for idx, step in enumerate(steps):
            try:
                obj = step(obj, *args, **kwargs)
            except StepException as explain:
                if step.step_type == 'then':
                    return False, explain
                else:
                    # failed conditional i.e. not relevant
                    return None, explain
            if step.loop:
                for o in obj:
                    o_result, o_explain = self.loop(
                        o, steps[idx + 1:], *args, **kwargs)
                    if not o_result:
                        return o_result, o_explain
                return True, None
        return True, None

    def __call__(self, obj, *args, **kwargs):
        def output(res, msg):
            if kwargs.get('bdd_verbose'):
                return res, msg
            return res

        context = dict(kwargs)
        if 'bdd_verbose' in context:
            del context['bdd_verbose']

        res, msg = self.loop(obj, self.steps, *args, **context)
        return output(res, msg)


class Step:
    def __init__(self, step_dict, step_type, test):
        def _find_matching_expr(line):
            for regex, fn, loop in test.feature.tester.store.values():
                r = regex.match(line)
                if r:
                    return fn, loop, r.groups()
            msg = 'I didn\'t understand "{}"'.format(line)
            raise UnknownStepException(msg)

        self.test = test

        self.text = step_dict['text']
        self.step_type = step_type
        match = _find_matching_expr(self.text)
        self.expr_fn, self.loop, self.expr_groups = match

    def __str__(self):
        return '{} {}'.format(self.step_type.title(), self.text)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, str(self))

    def __call__(self, *args, **kwargs):
        if self.expr_groups:
            args = args + self.expr_groups
        return self.expr_fn(*args, **kwargs)


class BDDTester:
    def __init__(self, step_path):
        self._load_step_definitions(step_path)
        self.gherkinparser = GherkinParser()

    def _load_step_definitions(self, filepath):
        reload(utils)
        if six.PY3:
            SourceFileLoader('', filepath).load_module()
        else:
            load_source('', filepath)
        self.store = dict(utils.store)

    def load_feature(self, feature_filepath):
        with open(feature_filepath) as f:
            feature_txt = f.read()
        return self._gherkinify_feature(feature_txt)

    def _gherkinify_feature(self, feature_txt):
        feature_dict = self.gherkinparser.parse(feature_txt)['feature']
        return Feature(feature_dict, self)
