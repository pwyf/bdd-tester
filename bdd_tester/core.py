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
    def __init__(self, name, tests=None):
        self.name = name
        self.tests = tests if tests else []

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, str(self))


class Test:
    def __init__(self, name, feature, steps, tags):
        self.name = name
        self.feature = feature
        self.steps = steps
        self.tags = tags

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
    def __init__(self, step_type, step_text, store):
        def _find_matching_expr(line):
            for regex, fn, loop in store.values():
                r = regex.match(line)
                if r:
                    return fn, loop, r.groups()
            msg = 'I didn\'t understand "{}"'.format(line)
            raise UnknownStepException(msg)

        self.text = step_text
        self.step_type = step_type
        match = _find_matching_expr(step_text)
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
        feature_name = feature_dict['name']
        feature = Feature(feature_name)
        for test in feature_dict['children']:
            test_name = test['name']
            test_steps = test['steps']
            test_tags = [tag['name'][1:] for tag in test['tags']]
            steps = []
            step_type = 'given'
            for step in test_steps:
                if step['keyword'].lower().strip() == 'then':
                    step_type = 'then'
                steps.append(Step(step_type, step['text'], self.store))
            feature.tests.append(Test(test_name, feature, steps, test_tags))
        return feature
