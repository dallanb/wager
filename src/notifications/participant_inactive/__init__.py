from .schema import ParticipantInactiveSchema
from ..base import Base


class participant_inactive(Base):
    key = 'participant_inactive'
    schema = ParticipantInactiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, participant):
        data = cls.schema.dump({'participant': participant})
        return participant_inactive(data=data)
