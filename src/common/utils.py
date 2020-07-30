import json
import uuid as UUID
from time import time


def get_json(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except TypeError as e:
        return {}


def generate_hash(items):
    frozen = frozenset(items)
    return hash(frozen)


def time_now():
    return int(time() * 1000.0)


def generate_uuid():
    return UUID.uuid4()


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')
