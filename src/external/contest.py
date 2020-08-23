from .. import app

from . import Base


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.host = app.config['CONTEST_HOST']
        self.port = app.config['CONTEST_PORT']
        self.base_url = f'http://{self.host}:{self.port}'

    def get_contest(self, uuid):
        url = f'{self.base_url}/contests/{uuid}'
        res = self.get(url=url)
        return res.json()
