from datetime import date, datetime

from behave.formatter._registry import make_formatters
from behave.runner import Runner, Context
from behave.runner_util import parse_features, print_undefined_step_snippets
from behave.model import Examples, ScenarioOutline, Table
from lxml import etree


class DQRunner(Runner):
    def start(self, filepath):
        # initialise context.
        # [monkeypatched]
        self.context = Context(self)

        # setup 'today' date and add to context
        today_str = self.context.config.userdata.get('today')
        if today_str:
            self.context.today = datetime.strptime(today_str, '%Y-%m-%d').date()
        else:
            self.context.today = date.today()

        # parse the IATI XML
        try:
            doc = etree.parse(filepath)
        except OSError:
            raise Exception('{} is not a valid XML file'.format(filepath))
        except etree.XMLSyntaxError as e:
            raise Exception('Failed trying to parse {}'.format(filepath))

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
        # [monkeypatched]
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

        # [monkeypatched]
        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)
        return self.run_model()
