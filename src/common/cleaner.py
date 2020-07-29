from flask import g


class Cleaner:
    def __init__(self):
        self.logger = g.logger.getLogger(__name__)
