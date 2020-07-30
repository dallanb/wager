from flask import g
from .base import Base
from ..models import Course as CourseModel
from ..common import advanced_query
from .. import cache, db


class Course(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    @cache.memoize(10)
    def find_course_by_golf_canada_id(golf_canada_id=None):
        if not golf_canada_id:
            raise ValueError('Missing golf_canada_id')

        filters = [('equal', [('golf_canada_id', golf_canada_id)])]
        courses = advanced_query(model=CourseModel, filters=filters)
        return courses

    @staticmethod
    @cache.memoize(10)
    def find_course(uuid=None):
        filters = []
        if uuid:
            filters.append(('equal', [('uuid', uuid)]))

        courses = advanced_query(model=CourseModel, filters=filters)
        return courses
