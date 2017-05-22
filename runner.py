import sys

from behave.configuration import Configuration
from behave.formatter._registry import make_formatters
from behave.runner import Runner, Context
from behave.runner_util import parse_features, print_undefined_step_snippets
from behave.model import Examples, ScenarioOutline, Table
from lxml import etree


class DQRunner(Runner):
    def run_with_paths(self):

        self.context = Context(self)
        self.load_hooks()
        self.load_step_definitions()

        # -- ENSURE: context.execute_steps() works in weird cases (hooks, ...)
        # self.setup_capture()
        # self.run_hook('before_all', self.context)

        # -- STEP: Parse all feature files (by using their file location).
        feature_locations = [ filename for filename in self.feature_locations()
                                    if not self.config.exclude(filename) ]
        features = parse_features(feature_locations, language=self.config.lang)

        doc = self.context.config.userdata['doc']
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
    config = Configuration(args)
    if not config.format:
        config.format = [config.default_format]

    # hack. We use the existing arg parser, then
    # attempt to extract the XML file from the
    # parsed args.

    # eventually we can add our own arg parser here.
    if config.paths == []:
        print('Please provide an XML file to test')
        return 1
    filepath = config.paths.pop(0)

    try:
        doc = etree.parse(filepath)
    except OSError:
        print('{} is not a valid XML file'.format(filepath))
        return 1
    except etree.XMLSyntaxError as e:
        print('Failed trying to parse {}'.format(filepath))
        print('\n  ' + str(e))
        return 1

    config.userdata = {
        'doc': doc,
    }

    runner = DQRunner(config)
    failed = runner.run()

    if config.show_snippets and runner.undefined_steps:
        print_undefined_step_snippets(runner.undefined_steps,
                                      colored=config.color)

    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
