from bdd_tester import given, then, StepException


@given(r'text is a shopping list')
def given_shopping_list(text, **kwargs):
    if not text.strip().lower().startswith('shopping list'):
        msg = 'Not a shopping list'
        raise StepException(msg)
    return text


@then(r'"([^"]+)" should be present')
def then_should_be_present(haystack, needle, **kwargs):
    if needle.lower() not in haystack.lower():
        msg = '"{}" not found'.format(needle)
        raise StepException(msg)
    return haystack
