import logging
from http import HTTPStatus

from .base import Base
from ..common import WagerStatusEnum
from ..models import Wager as WagerModel


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wager_model = WagerModel

    def add(self, **kwargs):
        wager = self._init(model=self.wager_model, **kwargs)
        return self._add(instance=wager)

    def create(self, **kwargs):
        wager = self._init(model=self.wager_model, **kwargs)
        _ = self.notify(
            topic='wagers',
            value={'uuid': str(wager.uuid)},
            key='wager_created'
        )
        return self._save(instance=wager)

    def find(self, **kwargs):
        return self._find(model=self.wager_model, **kwargs)

    def _status_machine(self, prev_status, new_status):
        # cannot go from active to pending
        if WagerStatusEnum[prev_status] == WagerStatusEnum['active'] and WagerStatusEnum[
            new_status] == WagerStatusEnum['pending']:
            self.error(code=HTTPStatus.BAD_REQUEST)
        return True
