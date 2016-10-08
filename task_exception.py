class TaskException(Exception):

    def __init__(self, msg, value=None):
        Exception.__init__(self, msg)
        self.value = value

