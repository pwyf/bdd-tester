from os.path import join
import json

from behave.model import ScenarioOutline
from behave.formatter.base import Formatter, StreamOpener


class DQSummaryFormatter(Formatter):
    name = 'dq_summary'
    description = 'DQ summary formatter'

    def __init__(self, stream_opener, config):
        super(DQSummaryFormatter, self).__init__(stream_opener, config)
        self.stream = self.open()
        # initialise scores
        self.score = {}

    def close(self):
        self.stream.write(json.dumps(self.score, indent=4))
        self.stream.write('\n')
        self.close_stream()

    def result(self, step):
        if step.step_type == 'given':
            if step.status == 'failed':
                self.score[self.scenario_name]['not-relevant'] += 1
        else:
            if step.status == 'passed':
                self.score[self.scenario_name]['passed'] += 1
            else:
                self.score[self.scenario_name]['failed'] += 1

    def scenario(self, scenario):
        if not scenario._row or scenario._row.index == 1:
            self.scenario_name = scenario.name.split(' -- ')[0]
            # initialise score for scenario
            self.score[self.scenario_name] = {
                'passed': 0,
                'failed': 0,
                'not-relevant': 0,
            }

class DQLogFormatter(Formatter):
    name = 'dq_log'
    description = 'DQ log formatter'

    def result(self, step):
        if step.step_type == 'then':
            if step.status == 'failed':
                self.stream.write(str(step.exception) + '\n')

    def scenario(self, scenario):
        if not scenario._row or scenario._row.index == 1:
            # close the current stream
            self.close()

            # open a new output filestream,
            # using the scenario name
            scenario_name = scenario.name.split(' -- ')[0]
            filepath = '{}.output'.format(
                join('output', scenario_name.lower().replace(' ', '_'))
            )
            self.stream_opener = StreamOpener(filepath)
            self.open()
