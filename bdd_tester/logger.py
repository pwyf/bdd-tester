import logging


class Logger():
    def __init__(self, context):
        context.config.setup_logging(level=logging.ERROR, filename='error.log', filemode='w')
        self.context = context
        self.real_logger = logging.getLogger()

    def error(self, msg):
        if self.context.activity_id:
            activity_id = self.context.activity_id
        else:
            activity_id = 'Activity {}'.format(self.context.activity_idx)

        self.real_logger.error('{}: {}'.format(activity_id, msg))
