import datetime
import json
from os.path import join
import re


@given('an organisation file')
def step_impl(context):
    assert(context.filetype == 'org')

# NB the original PWYF test also checked non-empty
@then('`{xpath_expression}` should be present')
def step_impl(context, xpath_expression):
    vals = context.xml.xpath(xpath_expression)
    if len(vals) > 0:
        assert(True)
    else:
        assert(False)

@then('every `{xpath_expression}` should be on the {codelist} codelist')
def step_impl(context, xpath_expression, codelist):
    vals = context.xml.xpath(xpath_expression)

    if len(vals) == 0:
        assert(False)

    codelist_path = join('codelists', '2', codelist + '.json')
    with open(codelist_path) as f:
        j = json.load(f)
    codes = [x['code'] for x in j['data']]

    for val in vals:
        if val not in codes:
            assert(False)
    assert(True)

@then('at least one `{xpath_expression}` should be on the {codelist} codelist')
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

@given('the activity is current')
def step_impl(context):
    assert(True)
    # raise NotImplementedError('STEP: Given the activity is current')

@then('`{xpath_expression}` should have at least {reqd_chars:d} characters')
def step_impl(context, xpath_expression, reqd_chars):
    vals = context.xml.xpath(xpath_expression)
    if len(vals) == 0:
        assert(False)
    most_chars, most_str = max([(len(val), val) for val in vals])
    result = most_chars > reqd_chars
    assert(result)

@given('`{xpath_expression}` is one of {consts}')
def step_impl(context, xpath_expression, consts):
    consts_list = re.split(r', | or ', consts)
    vals = context.xml.xpath(xpath_expression)
    if len(vals) == 0:
        # explain = '{vals_explain} should be one of {const_explain}. However, the activity doesn\'t contain that element'
        assert(True)
        return
    for val in vals:
        if val in consts_list:
            # explain = '{vals_explain} is one of {const_explain} (it\'s {val})'
            assert(True)
            return
    # explain = '{vals_explain} is not one of {const_explain} (it\'s {val})'
    assert(False)

def mkdate(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def get_reference_date():
    return datetime.date.today()

@given('`{xpath_expression}` is at least {months_ahead:d} months ahead')
def step_impl(context, xpath_expression, months_ahead):
    dates = context.xml.xpath(xpath_expression)

    if len(dates) == 0:
        # explain = '`{xpath_expression}` is not present, so assuming it is not at least {months} months ahead'
        # explain = explain.format(xpath_expression=xpath_expression, months=months)
        assert(False)

    valid_dates = list(filter(lambda x: x, [mkdate(date_str) for date_str in dates]))
    if not valid_dates:
        # explain = '{date} does not use format YYYY-MM-DD, so assuming it is not at least {months} months ahead'
        # explain = explain.format(date=dates[0], months=months)
        assert(False)

    # prefix = '' if len(valid_dates) == 1 or max(valid_dates) == min(valid_dates) else 'the most recent '

    max_date = max(valid_dates)
    reference_date = get_reference_date()
    year_diff = max_date.year - reference_date.year
    month_diff = 12 * year_diff + max_date.month - reference_date.month
    if month_diff == months_ahead:
        assert(max_date.day > reference_date.day)
    else:
        assert(month_diff > months_ahead)

@given('`{xpath_expression}` is not {const}')
def step_impl(context, xpath_expression, const):
    vals = context.xml.xpath(xpath_expression)
    for val in vals:
        if val == const:
            assert(False)
    assert(True)

@then('`{xpath_expression}` should be available forward {period}')
def step_impl(context, xpath_expression, period):
    vals = context.xml.xpath(xpath_expression)
    reference_date = get_reference_date()

    def max_date(dates, default):
        dates = list(filter(lambda x: x is not None, [mkdate(d) for d in dates]))
        if dates == []:
            return default
        return max(dates)

    # Window start is from today onwards. We're only interested in budgets
    # that start or end after today.

    # Window period is for the next 365 days. We don't want to look later
    # than that; we're only interested in budgets that end before then.
    #
    # We get the latest date for end and start; 365 days fwd
    # if there are no dates

    def check_after(element, today):
        dates = element.xpath('period-start/@iso-date|period-end/@iso-date')
        dates = list(filter(lambda x: x is not None, [mkdate(d) for d in dates]))
        return any([date >= today for date in dates])

    def max_budget_length(element, max_budget_length):
        # NB this will error if there's no period-end/@iso-date
        try:
            start = mkdate(element.xpath('period-start/@iso-date')[0])
            end = mkdate(element.xpath('period-end/@iso-date')[0])
            within_length = ((end-start).days <= max_budget_length)
        except TypeError:
            return False
        return within_length

    # We set a maximum number of days for which a budget can last,
    # depending on the number of quarters that should be covered.
    if period == 'quarterly':
        max_days = 94
    else:
        # annually
        max_days = 370

    # A budget has to be:
    # 1) period-end after reference date
    # 2) a maximum number of days, depending on # of qtrs.
    for element in vals:
        after_ref = check_after(element, reference_date)
        within_length = max_budget_length(element, max_days)
        if after_ref and within_length:
            assert(True)
            return
    assert(False)

def either_or(context, tmpl, xpath_expressions):
    for xpath_expression in xpath_expressions:
        try:
            context.execute_steps(tmpl.format(
                expression=xpath_expression)
            )
            assert(True)
            return
        except AssertionError:
            pass
    assert(False)

@given('either `{xpath_expression1}` or `{xpath_expression2}` {statement}')
def step_impl(context, xpath_expression1, xpath_expression2, statement):
    xpath_expressions = [xpath_expression1, xpath_expression2]
    tmpl = 'given `{{expression}}` {statement}'.format(
        statement=statement,
    )
    either_or(context, tmpl, xpath_expressions)

@then('either `{xpath_expression1}` or `{xpath_expression2}` {statement}')
def step_impl(context, xpath_expression1, xpath_expression2, statement):
    xpath_expressions = [xpath_expression1, xpath_expression2]
    tmpl = 'then `{{expression}}` {statement}'.format(
        statement=statement,
    )
    either_or(context, tmpl, xpath_expressions)

@then('either {modifier} `{xpath_expression1}` or `{xpath_expression2}` {statement}')
def step_impl(context, modifier, xpath_expression1, xpath_expression2, statement):
    xpath_expressions = [xpath_expression1, xpath_expression2]
    tmpl = 'then {modifier} `{{expression}}` {statement}'.format(
        modifier=modifier,
        statement=statement,
    )
    either_or(context, tmpl, xpath_expressions)
