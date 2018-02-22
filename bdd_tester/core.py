from datetime import datetime

from gherkin.parser import Parser as GherkinParser
import six

from .exceptions import StepException


if six.PY3:
    from importlib.machinery import SourceFileLoader
else:
    from imp import load_source


class Feature:
    def __init__(self, name, tests):
        self.name = name
        self.tests = tests

    def __str__(self):
        return self.name


class Test:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def __str__(self):
        return self.name

    def __call__(self, activity, codelists={}, today=None, verbose=False):
        def output(res, msg):
            if verbose:
                return res, msg
            return res

        if today:
            today = datetime.strptime(today, '%Y-%m-%d').date()
        else:
            today = datetime.today().date()
        kwargs = {
            'codelists': codelists,
            'today': today,
        }
        for step in self.steps:
            result = True
            explain = ''
            try:
                step(activity, **kwargs)
            except StepException as e:
                result = False
                explain = str(e)
            if step.step_type == 'then':
                if result is False:
                    return output(result, explain)
            else:
                if not result:
                    # failed conditional i.e. not relevant
                    return output(None, explain)
                else:
                    # passed conditional
                    pass
        return output(True, '')


class Step:
    mappings = []

    def __init__(self, step_type, step_text):
        def _find_matching_expr(line):
            for regex, fn in self.mappings:
                r = regex.match(line)
                if r:
                    return fn, r.groups()
            print('I didn\'t understand "{}"'.format(line))

        self.text = step_text
        self.step_type = step_type
        fn, groups = _find_matching_expr(step_text)
        self.expr_fn, self.expr_groups = fn, groups

    def __str__(self):
        return '{} {}'.format(self.step_type.title(), self.text)

    def __call__(self, activity, **kwargs):
        if self.expr_groups:
            self.expr_fn(activity, *self.expr_groups, **kwargs)
        else:
            self.expr_fn(activity, **kwargs)


class BDDTester:
    def __init__(self, stepfile_filepath):
        self._load_step_definitions(stepfile_filepath)
        self.gherkinparser = GherkinParser()

    def _load_step_definitions(self, filepath):
        # TODO: This is not right! The mappings array
        # will be overwritten whenever a new step definitions
        # file is loaded.
        Step.mappings = []
        if six.PY3:
            SourceFileLoader('', filepath).load_module()
        else:
            load_source('', filepath)

    def load_feature(self, feature_txt):
        return self._gherkinify_feature(feature_txt)

    def _gherkinify_feature(self, feature_txt):
        feature = self.gherkinparser.parse(feature_txt)
        feature = feature['feature']
        feature_name = feature['name']
        tests = []
        for test in feature['children']:
            test_name = test['name']
            test_steps = test['steps']
            steps = []
            step_type = 'given'
            for step in test_steps:
                if step['keyword'].lower().strip() == 'then':
                    step_type = 'then'
                steps.append(Step(step_type, step['text']))
            tests.append(Test(test_name, steps))
        return Feature(feature_name, tests)
