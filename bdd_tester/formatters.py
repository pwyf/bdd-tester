from os.path import join
import json

from behave.model import ScenarioOutline
from behave.formatter.base import Formatter, StreamOpener


class DQSummaryFormatter(Formatter):
    name = 'dq_summary'
    description = 'DQ summary formatter'

    def __init__(self, stream_opener, config):
        super(DQSummaryFormatter, self).__init__(stream_opener, config)

        # setup output filepath
        filepath = join('output', config.userdata['filename'], stream_opener.name)
        self.stream_opener = StreamOpener(filepath)
        self.stream = self.open()

        # initialise scores
        self.score = {}

    def close(self):
        # dump results
        self.stream.write(json.dumps(self.score, indent=4))
        self.stream.write('\n')
        self.close_stream()

    def result(self, step):
        if step.step_type == 'then':
            if step.status == 'passed':
                self.score[self.scenario_name]['passed'] += 1
            else:
                self.score[self.scenario_name]['failed'] += 1
        else:
            if step.status == 'failed':
                # the condition failed
                self.score[self.scenario_name]['not-relevant'] += 1
            else:
                # we don't care about conditions that pass
                pass

    def feature(self, feature):
        # initialise score for scenarios
        for scenario in feature.scenarios:
            scenario_name = scenario.name.split(' -- ')[0]
            self.score[scenario_name] = {
                'passed': 0,
                'failed': 0,
                'not-relevant': 0,
            }

    def scenario(self, scenario):
        if not scenario._row or scenario._row.index == 1:
            self.scenario_name = scenario.name.split(' -- ')[0]

class DQLogFormatter(Formatter):
    name = 'dq_log'
    description = 'DQ log formatter'

    def __init__(self, stream_opener, config):
        super(DQLogFormatter, self).__init__(stream_opener, config)
        # setup the output filepath
        self.output_path = join('output', config.userdata['filename'])

    def result(self, step):
        if step.step_type == 'then':
            if step.status == 'failed':
                # log the exception
                self.stream.write(str(step.exception) + '\n')

    def scenario(self, scenario):
        if not scenario._row or scenario._row.index == 1:
            # close the current stream
            self.close()

            # open a new output filestream,
            # using the scenario name
            scenario_name = scenario.name.split(' -- ')[0]
            slugified_name = scenario_name.lower().replace(' ', '_')
            filepath = '{}.output'.format(
                join(self.output_path, slugified_name)
            )
            self.stream_opener = StreamOpener(filepath)
            self.open()
