import json
from bdd_tester.logger import Logger


def before_all(context):
    context.logger = Logger(context)

def before_scenario(context, scenario):
    if context.active_outline:
        # for scenario outlines, we set the relevant activity
        row = context.active_outline
        # fetch the relevant activity and set it on the context
        activity = context.activities[row.index-1]
        context.xml = activity
        try:
            context.activity_id = activity.xpath('iati-identifier/text()')[0]
        except:
            context.activity_id = None
        context.activity_idx = row.index
    else:
        context.xml = context.organisation
