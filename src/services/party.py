import logging
from .base import Base
from ..models import Party as PartyModel
from http import HTTPStatus


class Party(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.party_model = PartyModel

    def find(self, **kwargs):
        return self._find(model=self.party_model, **kwargs)

    def add(self, **kwargs):
        party = self._init(model=self.party_model, **kwargs)
        return self._add(instance=party)

    def create(self, **kwargs):
        party = self._init(model=self.party_model, **kwargs)
        return self._save(instance=party)

    def update(self, uuid, **kwargs):
        parties = self.find(uuid=uuid)
        if not parties.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        party = self.assign_attr(instance=parties.items[0], attr=kwargs)
        return self._save(instance=party)
