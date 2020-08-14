import logging
from .base import Base


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)

    def handle_event(self, key, data):
        self.logger.info(key)
        self.logger.info(data)
        return key
