from src import services

contest = None


###########
# Find
###########
def test_contest_find_by_contest_uuid(reset_db, get_contest_uuid, create_wager):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 1 contest
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    contest_service = services.ContestService()

    # find by contest_uuid
    global contest
    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.contest_uuid == contest_uuid


def test_contest_find_by_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 contest
    """
    contest_service = services.ContestService()

    # find by uuid
    global contest
    contests = contest_service.find(uuid=contest.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.uuid == contest.uuid


def test_contest_find_include_wager():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 contest
    """
    contest_service = services.ContestService()

    # find by uuid
    global contest
    contests = contest_service.find(uuid=contest.uuid, include=['wager'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.wager.uuid is not None
