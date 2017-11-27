import json


class StepException(Exception):
    def __str__(self):
        return self.errors

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
            'id': self.id,
            'errors': self.errors,
        })
