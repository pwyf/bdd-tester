from behave.configuration import Configuration

from bdd_tester.runner import DQRunner


def bdd_tester(filepath, **kwargs):
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

    # specify the summary formatter output filename
    command_args += ['--outfile', 'summary.output']

    # pass stuff to behave via user-defined variables
    if kwargs.get('today'):
        command_args += ['--define', 'today=' + kwargs.get('today')]
    command_args += ['--define', 'output_path=' + kwargs.get('output_path')]

    # specify the location of the test files (features)
    command_args += kwargs.get('features')

    # create a config instance
    config = Configuration(command_args, load_config=False)

    # construct the runner!
    runner = DQRunner(config)

    # get this show on the road
    runner.start(filepath)
