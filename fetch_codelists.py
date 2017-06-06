from os import makedirs
from os.path import join

import requests

'''
Script to fetch IATI codelists in json format and dump them in
/codelists, for use in some of the tests.

Usage: python fetch_codelists.py
'''
versions = (
    {
        'iati_version': '105',
        'codelist_version': 'clv2',
    }, {
        'iati_version': '202',
        'codelist_version': 'clv3',
    },
)
all_codelists_tmpl = 'http://iatistandard.org/{iati_version}/codelists/downloads/{codelist_version}/codelists.json'
codelist_tmpl = 'http://iatistandard.org/{iati_version}/codelists/downloads/{codelist_version}/json/en/{codelist_name}.json'
for version in versions:
    codelist_path = join('codelists', version['iati_version'][0])
    makedirs(codelist_path, exist_ok=True)
    all_codelists_url = all_codelists_tmpl.format(**version)
    print('fetching {}'.format(all_codelists_url))
    codelist_names = requests.get(all_codelists_url).json()
    for codelist_name in codelist_names:
        codelist_url = codelist_tmpl.format(codelist_name=codelist_name, **version)
        print('fetching {}'.format(codelist_url))
        r = requests.get(codelist_url)
        with open(join(codelist_path, codelist_name + '.json'), 'w') as f:
            f.write(r.text)
