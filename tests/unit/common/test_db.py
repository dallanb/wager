import pytest

from src.common import DB, Cleaner
from src.models import *
from tests.helpers import generate_uuid

db = DB()
cleaner = Cleaner()
contest_uuid = pytest.contest_uuid


def test_init(reset_db):
    """
    GIVEN a db instance
    WHEN calling the init method of the db instance on the Contest model
    THEN it should return the contest instance
    """
    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    assert cleaner.is_mapped(instance) == instance
    assert cleaner.is_uuid(instance.contest_uuid) is not None
    assert instance.contest_uuid == contest_uuid

    db.rollback()


def test_count():
    """
    GIVEN a db instance
    WHEN calling the count method of the db instance on the Contest model
    THEN it should return the number of contest instances
    """
    count = db.count(model=Contest)
    assert count == 0

    contest = db.init(model=Contest, contest_uuid=contest_uuid)
    _ = db.save(instance=contest)
    count = db.count(model=Contest)
    assert count == 1


def test_add(reset_db):
    """
    GIVEN a db instance
    WHEN calling the add method of the db instance on a contest instance
    THEN it should add a contest instance to the database
    """
    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    contest = db.add(instance=instance)
    assert cleaner.is_uuid(contest.contest_uuid) is not None
    assert contest.contest_uuid == contest_uuid

    db.rollback()
    assert db.count(model=Contest) == 0


def test_commit(reset_db):
    """
    GIVEN a db instance
    WHEN calling the commit method of the db instance on a contest instance
    THEN it should add a contest instance to the database
    """
    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    contest = db.add(instance=instance)
    assert cleaner.is_uuid(contest.contest_uuid) is not None
    assert contest.contest_uuid == contest_uuid

    db.rollback()
    assert db.count(model=Contest) == 0

    _ = db.add(instance=instance)
    db.commit()
    assert db.count(model=Contest) == 1

    instance_0 = db.init(model=Contest, contest_uuid=generate_uuid())
    instance_1 = db.init(model=Contest, contest_uuid=generate_uuid())
    instance_2 = db.init(model=Contest, contest_uuid=generate_uuid()
                         )
    db.add(instance=instance_0)
    db.add(instance=instance_1)
    db.add(instance=instance_2)
    db.commit()
    assert db.count(model=Contest) == 4


def test_save(reset_db):
    """
    GIVEN a db instance
    WHEN calling the save method of the db instance on a contest instance
    THEN it should add a contest instance to the database
    """
    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    assert cleaner.is_uuid(instance.contest_uuid) is not None
    assert instance.contest_uuid == contest_uuid
    contest = db.save(instance=instance)
    assert db.count(model=Contest) == 1
    assert contest.contest_uuid == contest_uuid


def test_find():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance
    THEN it should find a contest instance from the database
    """
    result = db.find(model=Contest)
    assert result.total == 1
    assert len(result.items) == 1

    result = db.find(model=Contest, contest_uuid=generate_uuid())
    assert result.total == 0


def test_destroy():
    """
    GIVEN a db instance
    WHEN calling the destroy method of the db instance on a contest instance
    THEN it should remove the contest instance from the database
    """
    result = db.find(model=Contest)
    assert result.total == 1
    assert len(result.items) == 1
    instance = result.items[0]

    assert db.destroy(instance=instance)
    assert db.count(model=Contest) == 0


def test_rollback(reset_db):
    """
    GIVEN a db instance
    WHEN calling the rollback method of the db instance
    THEN it should rollback a contest instance from being inserted the database
    """
    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    db.rollback()
    db.commit()
    assert db.count(model=Contest) == 0

    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    db.save(instance=instance)
    db.rollback()
    assert db.count(model=Contest) == 1


def test_clean_query(reset_db):
    """
    GIVEN a db instance
    WHEN calling the clean_query method of the db instance
    THEN it should return a query
    """
    query = db.clean_query(model=Contest)
    assert query is not None


def test_run_query(reset_db):
    """
    GIVEN a db instance
    WHEN calling the run_query method of the db instance with a valid query
    THEN it should return the query result
    """
    instance = db.init(model=Contest, contest_uuid=contest_uuid)
    db.save(instance=instance)
    query = db.clean_query(model=Contest)
    contests = db.run_query(query=query)
    assert contests.total == 1


def test_equal_filter(reset_db, seed_wager, seed_party, seed_participant, seed_payouts):
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with an equal filter
    THEN it should return the query result
    """
    contests = db.find(model=Contest, contest_uuid=contest_uuid)
    assert contests.total == 1

    contest = contests.items[0]
    contests = db.find(model=Contest, contest_uuid=contest_uuid)
    assert contests.items[0] == contest


def test_nested_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a nested filter
    THEN it should return the query result
    """

    contests = db.find(model=Contest, nested={'wager': {'status': 'active'}})
    assert contests.total == 1


def test_within_filter(create_wager):
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with a within filter
    THEN it should return the query result
    """
    contest = db.init(model=Contest, contest_uuid=generate_uuid(), buy_in=5.0)
    db.save(instance=contest)

    contests = db.find(model=Contest)
    assert contests.total == 2

    contests = db.find(model=Contest, within={'buy_in': [5.0]})
    assert contests.total == 2

# def test_has_key_filter():
#     """
#     GIVEN a db instance
#     WHEN calling the find method of the db instance with a has_key filter
#     THEN it should return the query result
#     """
#     
#
#     contests = db.find(model=Contest)
#     assert contests.total == 2
#
#     contests = db.find(model=Contest, has_key={'uuid': pytest.contest.contest_uuid})
#     assert contests.total == 0
