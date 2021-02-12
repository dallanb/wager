from uuid import UUID

from iso4217 import Currency
from sqlalchemy.orm.base import object_mapper
from sqlalchemy.orm.exc import UnmappedInstanceError


class Cleaner:
    @classmethod
    def is_mapped(cls, v):
        if v is None:
            return v
        try:
            object_mapper(v)
        except UnmappedInstanceError:
            return None
        return v

    @classmethod
    def is_id(cls, v):
        if v is None:
            return v
        return cls.is_int(v, 1)

    @classmethod
    def is_string(cls, v, min_length=0, max_length=2000):
        if v is None:
            return v
        if not isinstance(v, str):
            return None
        if len(v) < min_length or len(v) > max_length:
            return None
        return v

    @classmethod
    def is_text(cls, v, min_length=0, max_length=4000):
        if v is None:
            return v
        if not isinstance(v, str):
            return None
        if len(v) < min_length or len(v) > max_length:
            return None
        return v

    @classmethod
    def is_int(cls, v, min_count=-9999999999, max_count=9999999999):
        if v is None:
            return v
        if isinstance(v, str) and v.isdigit():
            v = int(v)
        if not isinstance(v, int):
            return None
        if min_count is not None and v < min_count:
            return None
        if max_count is not None and v > max_count:
            return None
        return v

    @classmethod
    def is_uuid(cls, v):
        if v is None:
            return v
        try:
            if isinstance(v, UUID):
                v = str(v)
            uuid_v = UUID(v)
        except ValueError:
            return None
        except AttributeError:
            return None
        if not str(uuid_v) == v:
            return None
        return uuid_v

    @classmethod
    def is_list(cls, v):
        if v is None:
            return v
        if not isinstance(v, list):
            return None
        return v

    @classmethod
    def is_dict(cls, v):
        if v is None:
            return v
        if not isinstance(v, dict):
            return None
        return v

    @classmethod
    def is_currency(cls, v):
        if v is None:
            return v
        try:
            Currency(v)
        except ValueError:
            return None
        return v

    @classmethod
    def is_float(cls, v):
        if v is None:
            return v
        if not isinstance(v, float):
            return None
        return v

    @classmethod
    def is_num(cls, v):
        if v is None:
            return v
        if cls.is_float(v) is None and cls.is_int(v) is None:
            return None
        return v
