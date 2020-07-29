from flask import g
from .base import Base
from ..models import Course as CourseModel
from ..common import advanced_query
from .. import cache


class Course(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    @cache.memoize(10)
    def find_course(uuid=None):
        filters = []
        if uuid:
            filters.append(('equal', [('uuid', uuid)]))

        courses = advanced_query(model=CourseModel, filters=filters)
        return courses
