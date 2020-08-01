from ..models import Course as CourseModel
from ..common.db import find
from ..common.cache import cache


@cache.memoize(timeout=100)
def find_course_by_golf_canada_id(golf_canada_id):
    return find(model=CourseModel, golf_canada_id=golf_canada_id, single=True)


@cache.memoize(timeout=100)
def find_course_by_uuid(uuid):
    return find(model=CourseModel, uuid=uuid, single=True)
