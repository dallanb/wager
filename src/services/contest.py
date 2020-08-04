from ..models import Contest as ContestModel, ContestSchema
from ..common.db import find, save, init, destroy, count, tablename
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_contest():
    return count(ContestModel)


def find_contest(**kwargs):
    return find(model=ContestModel, **kwargs)


@cache.memoize(timeout=1000)
def find_contest_by_uuid(uuid):
    return find(model=ContestModel, uuid=uuid, single=True)


def init_contest(**kwargs):
    return init(model=ContestModel, **kwargs)


def save_contest(contest):
    unmemoize(find_contest_by_uuid, uuid=contest.uuid)
    unmemoize(count_contest)
    return save(instance=contest)


def destroy_contest(contest):
    unmemoize(find_contest_by_uuid, uuid=contest.uuid)
    unmemoize(count_contest)
    return destroy(instance=contest)


def dump_contest(contest, **kwargs):
    return ContestSchema().dump(contest, **kwargs)
