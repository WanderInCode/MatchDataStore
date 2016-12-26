import logging


class Utils:

    _Session = None

    @classmethod
    def set_session_make(cls, Session):
        cls._Session = Session

    @classmethod
    def get_session_make(cls):
        return cls._Session

logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    level=20)
logger = logging.getLogger()

players = dict()
