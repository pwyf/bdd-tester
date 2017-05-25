from datetime import date, datetime
import re


def get_reference_date():
    return date.today()

@given('an IATI activity')
def step_impl(context):
    assert(True)

@then('every `{xpath_expression}` should match the regex `{regex_str}`')
def step_impl(context, xpath_expression, regex_str):
    vals = context.xml.xpath(xpath_expression)
    regex = re.compile(regex_str)
    for val in vals:
        assert(bool(regex.search(val)))

@given('`{xpath_expression}` is present')
def step_impl(context, xpath_expression):
    vals = context.xml.xpath(xpath_expression)
    if len(vals) > 0:
        assert(True)
    else:
        assert(False)

@then('`{xpath_expression}` should not be present')
def step_impl(context, xpath_expression):
    vals = context.xml.xpath(xpath_expression)
    if len(vals) == 0:
        assert(True)
    else:
        assert(False)

@given('`{xpath_expression}` is a valid date')
def step_impl(context, xpath_expression):
    vals = context.xml.xpath(xpath_expression)
    for val in vals:
        try:
            _ = datetime.strptime(val, '%Y-%m-%d')
            assert(True)
            return
        except ValueError:
            assert(False)
    assert(False)

@then('`{xpath_expression1}` should be chronologically before `{xpath_expression2}`')
def step_impl(context, xpath_expression1, xpath_expression2):
    val1 = context.xml.xpath(xpath_expression1)[0]
    val2 = context.xml.xpath(xpath_expression2)[0]

    less = datetime.strptime(val1, '%Y-%m-%d').date()
    more = datetime.strptime(val2, '%Y-%m-%d').date()
    assert(less <= more)

@then('`{xpath_expression}` should be today, or in the past')
def step_impl(context, xpath_expression):
    val = context.xml.xpath(xpath_expression)[0]
    date = datetime.strptime(val, '%Y-%m-%d').date()
    assert(date <= get_reference_date())
