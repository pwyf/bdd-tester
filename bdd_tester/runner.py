from datetime import date, datetime
from os.path import dirname, join

from behave.formatter._registry import make_formatters
from behave.runner import Runner, Context, exec_file
from behave.runner_util import parse_features, print_undefined_step_snippets
from behave.model import Examples, ScenarioOutline, Table


class DQRunner(Runner):
    def start(self, doc):
        # initialise context.
        # [monkeypatched]
        self.context = Context(self)

        # setup 'today' date and add to context
        today_str = self.context.config.userdata.get('today')
        if today_str:
            self.context.today = datetime.strptime(today_str, '%Y-%m-%d').date()
        else:
            self.context.today = date.today()

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
            condition = self.context.config.userdata.get('condition')
            if condition:
                self.context.activities = doc.xpath('//iati-activity/{}'.format(condition))
            else:
                self.context.activities = doc.xpath('//iati-activity')
            self.context.organisation = None

        # [monkeypatched]
        self.run()
        if self.config.show_snippets and self.undefined_steps:
            print_undefined_step_snippets(self.undefined_steps,
                                          colored=self.config.color)

    def run_with_paths(self):
        self.load_hooks()
        self.load_step_definitions()
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

        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)
        return self.run_model()

    def load_hooks(self):
        # load environment.py from here - not steps directory
        path_to_env = join(dirname(__file__), 'environment.py')
        exec_file(path_to_env, self.hooks)
