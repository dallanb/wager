from .schema import PayoutUpdatedSchema
from ..base import Base


class payout_updated(Base):
    key = 'payout_updated'
    schema = PayoutUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, wager):
        data = cls.schema.dump({'wager': wager})
        return payout_updated(data=data)
