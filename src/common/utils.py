import json


def get_json(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except TypeError as e:
        return {}


def generate_hash(items):
    frozen = frozenset(items)
    return hash(frozen)
