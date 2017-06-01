import json

from behave.model import ScenarioOutline
from behave.formatter.base import Formatter


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

    def feature(self, feature):
        self.current_feature = feature

    def eof(self):
        for scenario in self.current_feature:
            if isinstance(scenario, ScenarioOutline):
                self.process_scenario_outline(scenario)
            else:
                self.process_scenario(scenario)

    def process_scenario(self, scenario):
        scenario_outline_name = scenario.name.split(' -- ')[0]
        if scenario_outline_name not in self.score:
            # initialise score for scenario
            self.score[scenario_outline_name] = {
                'passed': 0,
                'failed': 0,
                'not-relevant': 0,
            }
        for x in scenario.steps:
            if x.status == 'failed':
                if x.step_type == 'given':
                    self.score[scenario_outline_name]['not-relevant'] += 1
                else:
                    self.score[scenario_outline_name]['failed'] += 1
                return
        self.score[scenario_outline_name]['passed'] += 1

    def process_scenario_outline(self, scenario_outline):
        for scenario in scenario_outline.scenarios:
            self.process_scenario(scenario)
