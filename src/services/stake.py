import logging
from .base import Base
from ..models import Stake as StakeModel
from http import HTTPStatus


class Stake(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.stake_model = StakeModel

    def find(self, **kwargs):
        return Base.find(self, model=self.stake_model, **kwargs)

    def create(self, **kwargs):
        stake = self.init(model=self.stake_model, **kwargs)
        return self.save(instance=stake)

    def update(self, uuid, instance, **kwargs):
        stakes = self.find(uuid=uuid)
        if not stakes.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        stake = self.assign_attr(instance=stakes.items[0], attr=kwargs)
        return self.save(instance=stake)

    def destroy(self, uuid):
        stakes = self.find(uuid=uuid)
        if not stakes.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=stakes.items[0])
