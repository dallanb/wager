from flask import g
from .base import Base
from ..models import Course as CourseModel


class Course(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)
