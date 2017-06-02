import json


def before_scenario(context, scenario):
    if context.active_outline:
        # for scenario outlines, we set the relevant activity
        row = context.active_outline
        # fetch the relevant activity and set it on the context
        activity = context.activities[row.index-1]
        context.xml = activity
    else:
        context.xml = context.organisation
