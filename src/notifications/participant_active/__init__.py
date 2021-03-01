from .schema import ParticipantActiveSchema
from ..base import Base


class participant_active(Base):
    key = 'participant_active'
    schema = ParticipantActiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, participant):
        data = cls.schema.dump({'participant': participant})
        return participant_active(data=data)
