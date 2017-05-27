from behave.configuration import Configuration
from behave.formatter._registry import make_formatters
from behave.runner import Runner, Context
from behave.runner_util import parse_features, print_undefined_step_snippets
from behave.model import Examples, ScenarioOutline, Table
from lxml import etree


class DQRunner(Runner):
    def __init__(self, args=[]):
        # hack. We use the existing arg parser, then
        # attempt to extract the XML file from the
        # parsed args.

        # eventually we can add our own arg parser here.
        config = Configuration(args)
        if not config.format:
            config.format = [config.default_format]

        super(DQRunner, self).__init__(config)

    def run_file(self, filepath):
        if not filepath:
            raise Exception('Please provide an XML file to test')

        try:
            doc = etree.parse(filepath)
        except OSError:
            raise Exception('{} is not a valid XML file'.format(filepath))
        except etree.XMLSyntaxError as e:
            raise Exception('Failed trying to parse {}'.format(filepath))
        self.context = Context(self)
        self.context.doc = doc

        failed = self.run()

        if self.config.show_snippets and self.undefined_steps:
            print_undefined_step_snippets(self.undefined_steps,
                                          colored=self.config.color)

        if failed:
            raise Exception

        return self.context.score

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

        doc = self.context.doc
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

            activities = self.context.activities
            rows = [['Activity {}'.format(idx)] for idx, _ in enumerate(activities)]
            table = Table(
                ['activity name'],
                line=0,
                rows=rows,
            )
            examples = Examples('', 0, 'Example', 'Activity', table=table)
            # Hack to run the scenario once for each activity
            for feature in features:
                for scenario in feature.scenarios:
                    if type(scenario) is ScenarioOutline:
                        scenario.examples.append(examples)
        self.features.extend(features)

        # -- STEP: Run all features.
        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)
        return self.run_model()

def main(args=[]):
    if len(args) > 0 and len(args[0]) > 0 and args[0][0] != '-':
        filepath = args.pop(0)
    else:
        filepath = None

    runner = DQRunner(args)
    failed = False
    try:
        runner.run_file(filepath)
    except:
        failed = True

    return 1 if failed else 0
