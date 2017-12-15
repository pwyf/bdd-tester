import csv
from datetime import datetime
from importlib.machinery import SourceFileLoader
from os.path import join

from lxml import etree

from . import utils


def bdd_tester(step_definitions_path, features, **kwargs):
    default_output_path = 'output'
    if kwargs.get('output_path'):
        output_path = kwargs.get('output_path')
    else:
        output_path = default_output_path
    filters = kwargs.get('filters', [])

    # condition = kwargs.get('condition')
    # if condition:
    #     condition_parts = condition.split('/')
    #     go_backs = len([x for x in condition_parts if x == '..'])
    #     condition_parts = condition_parts + \
    #         ['..'] * (len(condition_parts) - 2 * go_backs)
    #     condition = '/'.join(condition_parts)

    # remarkably, this seems to be sufficient
    SourceFileLoader('', step_definitions_path).load_module()

    test_related_kwargs = {
        'today': kwargs.get('today', datetime.today()),
        'codelists': kwargs.get('codelists', {}),
    }
    features = utils.load_features(features, **test_related_kwargs)
    filters = utils.load_features(filters, **test_related_kwargs)

    # parse the XML
    filepath = kwargs.get('filepath')
    if filepath:
        try:
            doc = etree.parse(filepath)
        except OSError:
            raise Exception('{} is not a valid XML file'.format(filepath))
        except etree.XMLSyntaxError:
            raise Exception('Failed trying to parse {}'.format(filepath))
    else:
        doc = kwargs.get('etree')
    activities = doc.xpath('//iati-activity')

    for test_name, test in filters:
        filtered_activities = []
        for activity in activities:
            try:
                utils.mappings[7][1](activity)
            except:
                continue
            filtered_activities.append(activity)
        activities = filtered_activities

    scores = {}
    for test_name, test in features:
        score = {'passed': 0, 'failed': 0, 'not-relevant': 0}
        filename = join(output_path, utils.slugify(test_name) + '.csv')
        with open(filename, 'w') as f:
            w = csv.writer(f)
            w.writerow(('IATI Identifier', 'Message'))
            for activity in activities:
                output = test(activity)
                if output[0] is False:
                    score['failed'] += 1
                    iati_id = activity.xpath('iati-identifier/text()')[0]
                    w.writerow((iati_id, output[1]))
                elif output[0] is True:
                    score['passed'] += 1
                else:
                    score['not-relevant'] += 1
        scores[test_name] = score

    return scores
