from flask import g
from .base import Base
from ..models import WagerStatus as WagerStatusModel
from ..common import WagerStatusEnum


class WagerStatus(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def find_status(status_enum):
        if status_enum is None:
            raise ValueError('Missing status')
        status = WagerStatusModel.query.filter(WagerStatusModel.name == status_enum).first()
        return status
