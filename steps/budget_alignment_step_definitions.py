import json
from os.path import join


@given('at least one `{xpath_expression}` is on the {codelist} codelist')
def step_impl(context, xpath_expression, codelist):
    vals = context.xml.xpath(xpath_expression)

    if len(vals) == 0:
        assert(False)

    codelist_path = join('codelists', '2', codelist + '.json')
    with open(codelist_path) as f:
        j = json.load(f)
    codes = [x['code'] for x in j['data']]

    for val in vals:
        if val in codes:
            assert(True)
            return
    assert(False)
