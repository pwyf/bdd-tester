import json



def before_scenario(context, scenario):
    if context.active_outline:
        # for scenario outlines, we set the relevant activity
        row = context.active_outline
        # extract the activity number
        activity_num = int(row.cells[0].split()[-1])
        # fetch the relevant activity and set it on the context
        activity = context.activities[activity_num]
        context.xml = activity
    else:
        context.xml = context.organisation
