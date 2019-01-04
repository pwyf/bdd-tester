from gherkin.parser import Parser as GherkinParser
import six

from .exceptions import StepException, UnknownStepException


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

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, str(self))


class Test:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, str(self))

    def __call__(self, *args, **kwargs):
        def output(res, msg):
            if kwargs.get('bdd_verbose'):
                return res, msg
            return res

        context = dict(kwargs)
        if 'bdd_verbose' in context:
            del context['bdd_verbose']

        for step in self.steps:
            result = True
            explain = ''
            try:
                step(*args, **context)
            except StepException as e:
                result = False
                explain = str(e)
            if step.step_type == 'then':
                if result is False:
                    return output(result, explain)
            else:
                if result is False:
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
            msg = 'I didn\'t understand "{}"'.format(line)
            raise UnknownStepException(msg)

        self.text = step_text
        self.step_type = step_type
        fn, groups = _find_matching_expr(step_text)
        self.expr_fn, self.expr_groups = fn, groups

    def __str__(self):
        return '{} {}'.format(self.step_type.title(), self.text)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__,
                                  self.step_type.title())

    def __call__(self, *args, **kwargs):
        if self.expr_groups:
            args = args + self.expr_groups
        self.expr_fn(*args, **kwargs)


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

    def load_feature(self, feature_filepath):
        with open(feature_filepath) as f:
            feature_txt = f.read()
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
