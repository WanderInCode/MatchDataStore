class TaskError(Exception):

    def __init__(self, *msg, **value):
        Exception.__init__(self, *msg)
        for key, value in value.items():
            self.key = value
