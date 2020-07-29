from flask import g
from .base import Base
from ..models import Stake as StakeModel
from ..common import advanced_query


class Stake(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def find_stake(uuid=None):
        filters = []
        if uuid:
            filters.append(('equal', [('uuid', uuid)]))

        wagers = advanced_query(model=StakeModel, filters=filters)
        return wagers

    @classmethod
    def create_stake(cls, **kwargs):
        currency = kwargs.get('currency', None)
        amount = kwargs.get('amount', None)

        if currency is None or amount is None:
            raise Exception('Missing required parms')

        stake = StakeModel(currency=currency, amount=amount)

    @classmethod
    def update_stake(cls, uuid, **kwargs):
        currency = kwargs.get('currency', None)
        amount = kwargs.get('amount', None)

        stake = cls.find_stake(uuid=uuid)
        if stake is None:
            raise Exception('Invalid UUID')

        if currency is not None:
            stake.currency = currency

        if amount is not None:
            stake.amount = amount

        g.db.session.commit()
