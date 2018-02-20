import json


class StepException(Exception):
    def __str__(self):
        return self.msg

    def __init__(self, xml, msg=''):
        self.msg = msg
        try:
            self.id = xml.xpath('iati-identifier/text()')[0]
        except:
            self.id = ''

    @property
    def json_output(self):
        return json.dumps({
            'id': self.id,
            'errors': self.errors,
        })
