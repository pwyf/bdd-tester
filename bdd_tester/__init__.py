import json
import sys

from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from lxml import etree
from six import StringIO

from bdd_tester.runner import DQRunner


def bdd_tester(filepath, features, **kwargs):
    default_output_path = 'output'

    # we'll add the behave args to this list
    command_args = []

    # disable the default summary
    command_args.append('--no-summary')

    # don't capture stdout. It doesn't matter, really...
    # but we don't need this (since we do it ourselves)
    command_args.append('--no-capture')

    # don't capture stderr either
    command_args.append('--no-capture-stderr')

    # but DO capture logging
    command_args.append('--logcapture')
    command_args += ['--logging-format', '%(levelname)s:%(message)s']
    if kwargs.get('logging_level'):
        command_args += ['--logging-level', kwargs.get('logging_level')]

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
    if kwargs.get('output_path'):
        output_path = kwargs.get('output_path')
    else:
        output_path = default_output_path
    command_args += ['--define', 'output_path=' + output_path]

    condition = kwargs.get('condition')
    if condition:
        condition_parts = condition.split('/')
        go_backs = len([x for x in condition_parts if x == '..'])
        condition_parts = condition_parts + ['..'] * (len(condition_parts) - 2 * go_backs)
        condition = '/'.join(condition_parts)
        command_args += ['--define', 'condition=' + condition]

    save_summary = kwargs.get('save_summary', False)
    if save_summary:
        # specify the summary formatter output filename
        command_args += ['--outfile', 'summary.output']

    # specify the location of the test files (features)
    command_args += features

    try:
        # create a config instance
        config = Configuration(command_args, load_config=False)

        if not save_summary:
            # summary formatter should output to a buffer
            summary = StringIO()
            config.outputs.insert(0, StreamOpener(stream=summary))

        # construct the runner!
        runner = DQRunner(config)

        # parse the IATI XML
        try:
            doc = etree.parse(filepath)
        except OSError:
            raise Exception('{} is not a valid XML file'.format(filepath))
        except etree.XMLSyntaxError as e:
            raise Exception('Failed trying to parse {}'.format(filepath))

        # get this show on the road
        runner.start(doc)

        if not save_summary:
            # dump summary formatter buffer
            return json.loads(summary.getvalue())
    except:
        if not save_summary:
            # something went wrong; dump summary formatter buffer
            print(summary.getvalue())
        raise
