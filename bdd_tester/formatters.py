from os.path import join
import json

from behave.formatter.base import Formatter, StreamOpener

from . import exceptions


def get_scenario_name(scenario):
    return scenario.name.split(' -- ')[0]


class DQSummaryFormatter(Formatter):
    name = 'dq_summary'
    description = 'DQ summary formatter'

    def __init__(self, stream_opener, config):
        super(DQSummaryFormatter, self).__init__(stream_opener, config)

        if stream_opener.name:
            # setup output file
            output_file = join(config.userdata['output_path'],
                               stream_opener.name)
            self.stream_opener = StreamOpener(output_file)
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
            scenario_name = get_scenario_name(scenario)
            self.score[scenario_name] = {
                'passed': 0,
                'failed': 0,
                'not-relevant': 0,
            }

    def scenario(self, scenario):
        if not scenario._row or scenario._row.index == 1:
            self.scenario_name = get_scenario_name(scenario)


class DQJSONFormatter(Formatter):
    '''Produce json output files containing a single array of JSON objects

    This formatter outputs one json file per scenario. Each file contains
    a json dump of an array of json objects. Each object contains the rule
    error paths for individual ids (activities) for the given scenario.
    '''
    name = 'dq_json'
    description = 'DQ JSON formatter'

    def __init__(self, stream_opener, config):
        super(DQJSONFormatter, self).__init__(stream_opener, config)
        self.close()
        self.output_path = config.userdata['output_path']
        self.output_file_open = False

    def result(self, step):
        if step.step_type == 'then':
            if step.status == 'failed':
                if not self.output_file_open:
                    # open a new output filestream
                    self.stream_opener = StreamOpener(self.output_file)
                    self.open()
                    # start of file
                    self.stream.write('[')
                    self.output_file_open = True
                else:
                    # append json output to the streamed file
                    self.stream.write(',')
                if type(step.exception) is exceptions.StepException:
                    self.stream.write(step.exception.json_output)
                else:
                    raise step.exception

    def _set_output_file(self, scenario):
        def slugify(inp):
            out = inp.lower().strip().replace(' ', '_')
            out = ''.join(c for c in out if c.isalnum() or c == '_')
            return out

        scenario_name = get_scenario_name(scenario)
        slugified_name = slugify(scenario_name)
        self.output_file = '{}.json'.format(
            join(self.output_path, slugified_name)
        )

    def scenario(self, scenario):
        if not scenario._row or scenario._row.index == 1:
            if self.output_file_open:
                # tail of file
                self.stream.write(']')
                self.close()
                self.output_file_open = False

            # set the new output filename, but don't open
            # the stream until we have some results
            self._set_output_file(scenario)
