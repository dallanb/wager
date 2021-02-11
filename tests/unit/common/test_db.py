from src.common import DB, Cleaner
from src.models import *
from tests.helpers import generate_uuid

db = DB()
cleaner = Cleaner()


def test_init(reset_db):
    """
    GIVEN a db instance
    WHEN calling the init method of the db instance on the Wager model
    THEN it should return the wager instance
    """
    instance = db.init(model=Wager, status='active')
    assert cleaner.is_mapped(instance) == instance
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.status == 'active'

    db.rollback()


def test_count():
    """
    GIVEN a db instance
    WHEN calling the count method of the db instance on the Wager model
    THEN it should return the number of wager instances
    """
    count = db.count(model=Wager)
    assert count == 0

    wager = db.init(model=Wager, status='active')
    _ = db.save(instance=wager)
    count = db.count(model=Wager)
    assert count == 1


def test_add(reset_db):
    """
    GIVEN a db instance
    WHEN calling the add method of the db instance on a wager instance
    THEN it should add a wager instance to the database
    """
    instance = db.init(model=Wager, status='active')
    wager = db.add(instance=instance)
    assert cleaner.is_uuid(wager.uuid) is not None
    assert wager.status == 'active'

    db.rollback()
    assert db.count(model=Wager) == 0


def test_commit(reset_db):
    """
    GIVEN a db instance
    WHEN calling the commit method of the db instance on a wager instance
    THEN it should add a wager instance to the database
    """
    instance = db.init(model=Wager, status='active')
    wager = db.add(instance=instance)
    assert cleaner.is_uuid(wager.uuid) is not None
    assert wager.status == 'active'

    db.rollback()
    assert db.count(model=Wager) == 0

    _ = db.add(instance=instance)
    db.commit()
    assert db.count(model=Wager) == 1

    instance_0 = db.init(model=Wager, status='active')
    instance_1 = db.init(model=Wager, status='active')
    instance_2 = db.init(model=Wager, status='active')
    db.add(instance=instance_0)
    db.add(instance=instance_1)
    db.add(instance=instance_2)
    db.commit()
    assert db.count(model=Wager) == 4


def test_save(reset_db):
    """
    GIVEN a db instance
    WHEN calling the save method of the db instance on a wager instance
    THEN it should add a wager instance to the database
    """
    instance = db.init(model=Wager, status='active')
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.status == 'active'
    wager = db.save(instance=instance)
    assert db.count(model=Wager) == 1
    assert wager.status.name == 'active'


def test_find():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance
    THEN it should find a wager instance from the database
    """
    result = db.find(model=Wager)
    assert result.total == 1
    assert len(result.items) == 1

    result = db.find(model=Wager, uuid=generate_uuid())
    assert result.total == 0


def test_destroy():
    """
    GIVEN a db instance
    WHEN calling the destroy method of the db instance on a wager instance
    THEN it should remove the wager instance from the database
    """
    result = db.find(model=Wager)
    assert result.total == 1
    assert len(result.items) == 1
    instance = result.items[0]

    assert db.destroy(instance=instance)
    assert db.count(model=Wager) == 0


def test_rollback(reset_db):
    """
    GIVEN a db instance
    WHEN calling the rollback method of the db instance
    THEN it should rollback a wager instance from being inserted the database
    """
    instance = db.init(model=Wager, status='active')
    db.rollback()
    db.commit()
    assert db.count(model=Wager) == 0

    instance = db.init(model=Wager, status='active')
    db.save(instance=instance)
    db.rollback()
    assert db.count(model=Wager) == 1

# def test_clean_query()