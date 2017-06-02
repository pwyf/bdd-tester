import json
import sys

from behave.configuration import Configuration
from six import StringIO

from bdd_tester.runner import DQRunner


def bdd_tester(filepath, features, **kwargs):
    default_output_path = 'output'

    # we'll add the behave args to this list
    command_args = []

    # disable the default summary
    command_args.append('--no-summary')

    # declare some custom formatters
    formatters = [
        'bdd_tester.formatters:DQSummaryFormatter',
        'bdd_tester.formatters:DQLogFormatter',
    ]
    for formatter in formatters:
        command_args += ['--format', formatter]

    # pass stuff to behave via user-defined variables
    if kwargs.get('today'):
        command_args += ['--define', 'today=' + kwargs.get('today')]
    if not kwargs.get('output_path'):
        output_path = default_output_path
    command_args += ['--define', 'output_path=' + output_path]

    capture_summary = kwargs.get('capture_summary', True)
    if not capture_summary:
        # specify the summary formatter output filename
        command_args += ['--outfile', 'summary.output']

    # specify the location of the test files (features)
    command_args += features

    # create a config instance
    config = Configuration(command_args, load_config=False)

    # construct the runner!
    runner = DQRunner(config)

    if capture_summary:
        # capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

    # get this show on the road
    runner.start(filepath)

    if capture_summary:
        result = sys.stdout
        sys.stdout = old_stdout
        # dump captured output
        return json.loads(result.getvalue())
