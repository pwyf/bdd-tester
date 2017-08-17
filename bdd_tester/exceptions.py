import json


class StepException(Exception):
    def __init__(self, context, errors=''):
        self.errors = errors
        self.id = ''
        try:
            self.id = context.xml.xpath('iati-identifier/text()')[0]
        except:
            pass

    @property
    def json_output(self):
        return json.dumps({
            'errors': self.errors,
            'id': self.id,
        })
