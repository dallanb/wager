import logging
from .base import Base
from ..external import Contest as ContestExternal
from ..models import Contest as ContestModel
from .wager import Wager


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.contest_external = ContestExternal()
        self.contest_model = ContestModel

    def find(self, **kwargs):
        return Base.find(self, model=self.contest_model, **kwargs)

    def create(self, **kwargs):
        contest = self.init(model=self.contest_model, **kwargs)
        return self.save(instance=contest)

    def handle_event(self, key, data):
        if key == 'contest_created':
            # create a wager
            contest = self.contest_external.get_contest(endpoint=data['endpoint'])
            contest_uuid = contest['data']['contests']['uuid']
            owner_uuid = contest['data']['contests']['owner_uuid']
            wager = Wager().create(owner_uuid=owner_uuid, status='active')
            _ = self.create(contest_uuid=contest_uuid, wager=wager)
