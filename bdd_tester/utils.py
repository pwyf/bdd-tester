import re
from glob import glob
from os.path import join

from gherkin.parser import Parser as GherkinParser


mappings = []


def given(pattern):
    def decorated(fn):
        mappings.append((re.compile(r'^{}$'.format(pattern)), fn))
        return fn
    return decorated


def then(pattern):
    def decorated(fn):
        mappings.append((re.compile(r'^{}$'.format(pattern)), fn))
        return fn
    return decorated


def find_matching_expr(mappings, line):
    for regex, fn in mappings:
        r = regex.match(line)
        if r:
            return fn, r.groups()
    print('I did not understand {}'.format(line))


def parse(ctx, **kwargs):
    def _parse(activity):
        for step_type, expr_fn, expr_groups in ctx:
            result = True
            try:
                if expr_groups:
                    expr_fn(activity, *expr_groups, **kwargs)
                else:
                    expr_fn(activity, **kwargs)
            except Exception as e:
                result = False
                explain = str(e)
            if step_type == 'given':
                if not result:
                    return None, explain
            else:
                if result:
                    return True, None
                else:
                    return False, explain
    return _parse


def gherkinify(feature_path):
    gherkins = []
    feature_files = glob(join(feature_path, '**', '*.feature'), recursive=True)
    parser = GherkinParser()
    for feature_file in feature_files:
        with open(feature_file, 'rb') as f:
            data = f.read().decode('utf8')
        gherkins.append(parser.parse(data))
    return gherkins


def load_features(feature_path, **kwargs):
    features = gherkinify(feature_path)

    out = []
    for feature in features:
        for test in feature['feature']['children']:
            test_name = test['name']
            test_steps = test['steps']
            ctx = []
            for step in test_steps:
                step_type = step['keyword'].lower().strip()
                expr_fn, expr_groups = find_matching_expr(
                    mappings, step['text'])
                ctx.append((step_type, expr_fn, expr_groups))
            out.append((test_name, parse(ctx, **kwargs)))
    return out


def slugify(inp):
    out = inp.lower().strip().replace(' ', '_')
    out = ''.join(c for c in out if c.isalnum() or c == '_')
    return out
