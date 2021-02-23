from .schema import StakeCreatedSchema
from ..base import Base


class stake_created(Base):
    key = 'stake_created'
    schema = StakeCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, stake):
        data = cls.schema.dump({'stake': stake})
        return stake_created(data=data)
