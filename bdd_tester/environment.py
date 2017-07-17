from os.path import join
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

def after_scenario(context, scenario):
    if context.log_capture:
        logs = context.log_capture.getvalue()
        with open(join(context.config.userdata['output_path'], 'log.output'), 'w') as f:
            f.write(logs)
