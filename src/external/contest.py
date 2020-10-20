from .. import app

from . import Base


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['CONTEST_URL']

    def get_contest(self, uuid):
        url = f'{self.base_url}/contests/{uuid}'
        res = self.get(url=url)
        return res.json()
