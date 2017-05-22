import json


def before_all(context):
    # initialise scores
    context.score = {}

def before_scenario(context, scenario):
    scenario_outline_name = scenario.name.split(' -- ')[0]
    if scenario_outline_name not in context.score:
        # initialise score for scenario
        context.score[scenario_outline_name] = {
            'passed': 0,
            'failed': 0,
            'not-relevant': 0,
        }

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

def after_scenario(context, scenario):
    scenario_outline_name = scenario.name.split(' -- ')[0]
    for x in scenario.steps:
        if x.status == 'failed':
            if x.step_type == 'given':
                context.score[scenario_outline_name]['not-relevant'] += 1
            else:
                context.score[scenario_outline_name]['failed'] += 1
            return
    context.score[scenario_outline_name]['passed'] += 1

def after_all(context):
    print(json.dumps(context.score, indent=4))
