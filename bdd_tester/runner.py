from datetime import date, datetime

from behave.configuration import Configuration
from behave.formatter._registry import make_formatters
from behave.runner import Runner, Context
from behave.runner_util import parse_features, print_undefined_step_snippets
from behave.model import Examples, ScenarioOutline, Table
from lxml import etree


class DQRunner(Runner):
    def __init__(self, filepath, **kwargs):
        # we'll add the behave args to this list
        command_args = []

        # set path to IATI file to test
        self.filepath = filepath

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

        super(DQRunner, self).__init__(config)

    def start(self):
        # initialise context
        self.context = Context(self)

        # setup 'today' date and add to context
        today_str = self.context.config.userdata.get('today')
        if today_str:
            self.context.today = datetime.strptime(today_str, '%Y-%m-%d').date()
        else:
            self.context.today = date.today()

        # parse the IATI XML
        try:
            doc = etree.parse(self.filepath)
        except OSError:
            raise Exception('{} is not a valid XML file'.format(self.filepath))
        except etree.XMLSyntaxError as e:
            raise Exception('Failed trying to parse {}'.format(self.filepath))

        # add IATI XML data to context
        organisations = doc.xpath('//iati-organisation')
        if len(organisations) > 0:
            self.context.filetype = 'org'
            # if this looks like an org file, set the organisation
            self.context.organisation = organisations[0]
            self.context.activities = []
        else:
            self.context.filetype = 'activity'
            # otherwise, set the activities
            self.context.activities = doc.xpath('//iati-activity')
            self.context.organisation = None

        # go!
        self.run()

        if self.config.show_snippets and self.undefined_steps:
            print_undefined_step_snippets(self.undefined_steps,
                                          colored=self.config.color)

    def run_with_paths(self):

        self.load_hooks()
        self.load_step_definitions()

        # -- ENSURE: context.execute_steps() works in weird cases (hooks, ...)
        # self.setup_capture()
        # self.run_hook('before_all', self.context)

        # -- STEP: Parse all feature files (by using their file location).
        feature_locations = [ filename for filename in self.feature_locations()
                                    if not self.config.exclude(filename) ]
        features = parse_features(feature_locations, language=self.config.lang)

        # Hack to run the scenario once for each activity
        if self.context.filetype == 'activity':
            activities = self.context.activities
            rows = [['Activity {}'.format(idx)] for idx, _ in enumerate(activities)]
            table = Table(
                ['activity name'],
                line=0,
                rows=rows,
            )
            examples = Examples('', 0, 'Example', 'Activity', table=table)
            for feature in features:
                for scenario in feature.scenarios:
                    if type(scenario) is ScenarioOutline:
                        scenario.examples.append(examples)
        self.features.extend(features)

        # -- STEP: Run all features.
        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)
        return self.run_model()
