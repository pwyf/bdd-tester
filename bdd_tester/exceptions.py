class StepException(Exception):
    def __init__(self, context, message=''):
        self.message = message
        try:
            id_ = context.xml.xpath('iati-identifier/text()')[0]
            self.message = '{}: {}'.format(id_, self.message)
        except:
            pass

    def __str__(self):
        return self.message
