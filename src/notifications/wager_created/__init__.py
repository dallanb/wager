from .schema import WagerCreatedSchema
from ..base import Base


class wager_created(Base):
    key = 'wager_created'
    schema = WagerCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, wager):
        data = cls.schema.dump({'wager': wager})
        return wager_created(data=data)
