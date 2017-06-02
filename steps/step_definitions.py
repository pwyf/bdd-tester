from datetime import datetime
import json
from os.path import join
import re

from bdd_tester.exceptions import StepException


@given('file is an organisation file')
def step_impl(context):
    if context.filetype != 'org':
        raise StepException(context, 'Not an organisation file')

# NB the original PWYF test also checked non-empty
@then('`{xpath_expression}` should be present')
def step_impl(context, xpath_expression):
    vals = context.xml.xpath(xpath_expression)
    if len(vals) == 0:
        msg = '`{}` not found'.format(xpath_expression)
        raise StepException(context, msg)

@then('every `{xpath_expression}` should be on the {codelist} codelist')
def step_impl(context, xpath_expression, codelist):
    vals = context.xml.xpath(xpath_expression)

    if len(vals) == 0:
        msg = '`{}` not found'.format(xpath_expression)
        raise StepException(context, msg)

    codelist_path = join('codelists', '2', codelist + '.json')
    with open(codelist_path) as f:
        j = json.load(f)
    codes = [x['code'] for x in j['data']]

    invalid_vals = []
    success = True
    for val in vals:
        if val not in codes:
            success = False
            invalid_vals.append(val)

    if not success:
        msg = '{invalid_vals} {isare} not on the {codelist} codelist'.format(
            invalid_vals=', '.join(invalid_vals),
            isare='is' if len(invalid_vals) == 1 else 'are',
            codelist=codelist,
        )
        raise StepException(context, msg)
    assert(True)

@then('at least one `{xpath_expression}` should be on the {codelist} codelist')
def step_impl(context, xpath_expression, codelist):
    vals = context.xml.xpath(xpath_expression)

    if len(vals) == 0:
        msg = '`{}` not found'.format(xpath_expression)
        raise StepException(context, msg)

    codelist_path = join('codelists', '2', codelist + '.json')
    with open(codelist_path) as f:
        j = json.load(f)
    codes = [x['code'] for x in j['data']]

    for val in vals:
        if val in codes:
            assert(True)
            return

    msg = '{invalid_vals} {isare} not on the {codelist} codelist'.format(
        invalid_vals=', '.join(vals),
        isare='is' if len(vals) == 1 else 'are',
        codelist=codelist,
    )
    raise StepException(context, msg)

@given('the activity is current')
def step_impl(context):
    assert(True)
    # raise NotImplementedError('STEP: Given the activity is current')

@then('`{xpath_expression}` should have at least {reqd_chars:d} characters')
def step_impl(context, xpath_expression, reqd_chars):
    vals = context.xml.xpath(xpath_expression)
    if len(vals) == 0:
        msg = '`{}` not found'.format(xpath_expression)
        raise StepException(context, msg)

    most_chars, most_str = max([(len(val), val) for val in vals])
    result = most_chars > reqd_chars

    if not result:
        msg = '`{}` has fewer than {} characters (it has {})'.format(
            xpath_expression,
            reqd_chars,
            most_chars,
        )
        raise StepException(context, msg)

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
    msg = '`{}` is not one of {} (it\'s {})'.format(
        xpath_expression,
        consts,
        val,
    )
    raise StepException(context, msg)

def mkdate(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

@given('`{xpath_expression}` is at least {months_ahead:d} months ahead')
def step_impl(context, xpath_expression, months_ahead):
    dates = context.xml.xpath(xpath_expression)

    if len(dates) == 0:
        msg = '`{}` is not present, so assuming it is not at least {} months ahead'.format(
            xpath_expression,
            months_ahead,
        )
        raise StepException(context, msg)

    valid_dates = list(filter(lambda x: x, [mkdate(date_str) for date_str in dates]))
    if not valid_dates:
        # explain = '{date} does not use format YYYY-MM-DD, so assuming it is not at least {months} months ahead'
        # explain = explain.format(date=dates[0], months=months)
        msg = '`{}` does not use format YYYY-MM-DD, so assuming it is not at least {} months ahead'.format(
            dates[0],
            months_ahead,
        )
        raise StepException(context, msg)

    prefix = '' if len(valid_dates) == 1 or max(valid_dates) == min(valid_dates) else 'the latest '

    max_date = max(valid_dates)
    year_diff = max_date.year - context.today.year
    month_diff = 12 * year_diff + max_date.month - context.today.month
    if month_diff == months_ahead:
        success = max_date.day > context.today.day
    else:
        success = month_diff > months_ahead
    if not success:
        msg = '{}`{}` is less than {} months ahead'.format(
            prefix,
            xpath_expression,
            months_ahead,
        )
        raise StepException(context, msg)

@given('`{xpath_expression}` is not {const}')
def step_impl(context, xpath_expression, const):
    vals = context.xml.xpath(xpath_expression)
    for val in vals:
        if val == const:
            msg = '`{}` is {}'.format(
                xpath_expression,
                val,
            )
            raise StepException(context, msg)
    assert(True)

@then('`{xpath_expression}` should be available forward {period}')
def step_impl(context, xpath_expression, period):
    vals = context.xml.xpath(xpath_expression)

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
        after_ref = check_after(element, context.today)
        within_length = max_budget_length(element, max_days)
        if after_ref and within_length:
            assert(True)
            return

    msg = 'Failed'
    raise StepException(context, msg)

def either_or(context, tmpl, xpath_expressions):
    exceptions = []
    for xpath_expression in xpath_expressions:
        try:
            context.execute_steps(tmpl.format(
                expression=xpath_expression)
            )
            assert(True)
            return
        except StepException as e:
            exceptions.append(e)

    msg = ' and '.join([str(e) for e in exceptions])
    raise StepException(context, msg)

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
