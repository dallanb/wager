from ..models import Course as CourseModel
from ..common.error import MissingParamError, InvalidTypeError
from ..common.cleaner import is_id, is_uuid
from ..common.db import find
from ..common.cache import cache


@cache.memoize(timeout=100)
def find_course_by_golf_canada_id(golf_canada_id=None):
    if not golf_canada_id:
        raise MissingParamError('golf_canada_id')
    if not is_id(golf_canada_id):
        raise InvalidTypeError('golf_canada_id', 'id')

    return find(model=CourseModel, golf_canada_id=golf_canada_id, single=True)


@cache.memoize(timeout=100)
def find_course_by_uuid(uuid=None):
    if not uuid:
        raise MissingParamError('uuid')
    if not is_uuid(uuid):
        raise InvalidTypeError('uuid', 'uuid')

    return find(model=CourseModel, uuid=uuid, single=True)
