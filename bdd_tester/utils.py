import re

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
                expr_fn(activity, *expr_groups, **kwargs)
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


def gherkinify(features):
    gherkins = []
    parser = GherkinParser()
    for feature_file in features:
        with open(feature_file, 'rb') as f:
            data = f.read().decode('utf8')
        gherkins.append(parser.parse(data))
    return gherkins


def load_features(features, **kwargs):
    features = gherkinify(features)

    out = []
    for feature in features:
        for test in feature['feature']['children']:
            test_name = test['name']
            test_steps = test['steps']
            ctx = []
            step_type = 'given'
            for step in test_steps:
                if step['keyword'] == 'Then ':
                    step_type = 'then'
                expr_fn, expr_groups = find_matching_expr(
                    mappings, step['text'])
                ctx.append((step_type, expr_fn, expr_groups))
            out.append((test_name, parse(ctx, **kwargs)))
    return out


def slugify(inp):
    out = inp.lower().strip().replace(' ', '_')
    out = ''.join(c for c in out if c.isalnum() or c == '_')
    return out
