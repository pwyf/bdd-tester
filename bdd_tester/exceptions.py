import json


class StepException(Exception):
    def __init__(self, xml, msg=''):
        self.msg = msg
        self.xml = xml

    @property
    def id(self):
        try:
            return self.id_
        except AttributeError:
            try:
                self.id_ = self.xml.find('iati-identifier').text
            except:
                self.id_ = '[no-identifier]'
        return self.id_

    def __str__(self):
        return '{}: {}'.format(self.id, self.msg)

    @property
    def json_output(self):
        return json.dumps({
            'id': self.id,
            'errors': self.errors,
        })
