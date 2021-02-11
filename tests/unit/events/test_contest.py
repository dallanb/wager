import time

from src import services, events
from tests.helpers import generate_uuid

base_service = services.Base()


def test_contest_owner_active_sync(reset_db, get_contest_uuid, get_member_uuid):
    """
    GIVEN 0 instance in the database
    WHEN directly calling event contest handle_event owner_active
    THEN it should add 1 wager instance, 1 contest instance, 2 payout instance, 1 party
    service, 1 participant service and 1 stake service
    """
    contest_uuid = get_contest_uuid()
    member_uuid = get_member_uuid()
    buy_in = 5.0
    payout_list = [0.60, 0.40]
    value = {
        'contest_uuid': str(contest_uuid),
        'participant_uuid': str(generate_uuid()),
        'member_uuid': str(member_uuid),
        'user_uuid': str(generate_uuid()),
        'owner_uuid': str(generate_uuid()),
        'league_uuid': str(generate_uuid()),
        'buy_in': buy_in,
        'payout': payout_list,
        'message': ''
    }

    events.Contest().handle_event(key='owner_active', data=value)

    wagers = services.WagerService().find()
    contests = services.ContestService().find()
    payouts = services.PayoutService().find()
    parties = services.PartyService().find()
    participants = services.ParticipantService().find()
    stakes = services.StakeService().find()

    assert wagers.total == 1
    assert contests.total == 1
    assert contests.items[0].contest_uuid == contest_uuid
    assert contests.items[0].buy_in == buy_in
    assert payouts.total == 2
    for payout in payouts.items:
        assert payout.proportion in payout_list
    assert parties.total == 1
    assert participants.total == 1
    assert participants.items[0].member_uuid == member_uuid
    assert stakes.total == 1
    assert stakes.items[0].amount == buy_in


def test_contest_participant_active_sync(get_contest_uuid):
    """
    GIVEN 1 wager instance, 1 contest instance, 2 payout instance, 1 party service, 1 participant service and 1 stake
    service instance in the database
    WHEN directly calling event contest handle_event participant_active
    THEN it should add 1 wager instance, 1 contest instance, 2 payout instance, 1 party
    service, 1 participant service and 1 stake service
    """
    contest_uuid = get_contest_uuid()
    member_uuid = generate_uuid()
    value = {
        'contest_uuid': str(contest_uuid),
        'participant_uuid': str(generate_uuid()),
        'member_uuid': str(member_uuid),
        'user_uuid': str(generate_uuid()),
        'owner_uuid': str(generate_uuid()),
        'league_uuid': str(generate_uuid()),
        'message': ''
    }

    events.Contest().handle_event(key='participant_active', data=value)

    wagers = services.WagerService().find()
    contests = services.ContestService().find()
    parties = services.PartyService().find()
    participants = services.ParticipantService().find()
    stakes = services.StakeService().find()

    assert wagers.total == 1
    assert contests.total == 1
    assert contests.items[0].contest_uuid == contest_uuid
    assert parties.total == 2
    assert participants.total == 2
    assert participants.items[0].member_uuid != participants.items[1].member_uuid
    assert stakes.total == 2
    assert stakes.items[0].amount == stakes.items[1].amount


def test_contest_owner_active_async(reset_db, get_contest_uuid, get_member_uuid):
    """
    GIVEN 0 instance in the database
    WHEN the CONTEST service notifies Kafka that an owner has been created
    THEN event contest handle_event owner_active adds 1 wager instance, 1 contest instance, 2 payout instance, 1 party
    service, 1 participant service and 1 stake service
    """
    contest_uuid = get_contest_uuid()
    member_uuid = get_member_uuid()
    buy_in = 5.0
    payout_list = [0.60, 0.40]
    value = {
        'contest_uuid': str(contest_uuid),
        'participant_uuid': str(generate_uuid()),
        'member_uuid': str(member_uuid),
        'user_uuid': str(generate_uuid()),
        'owner_uuid': str(generate_uuid()),
        'league_uuid': str(generate_uuid()),
        'buy_in': buy_in,
        'payout': payout_list,
        'message': ''
    }

    base_service.notify(topic='contests', value=value, key='owner_active')
    time.sleep(0.5)

    wagers = services.WagerService().find()
    contests = services.ContestService().find()
    payouts = services.PayoutService().find()
    parties = services.PartyService().find()
    participants = services.ParticipantService().find()
    stakes = services.StakeService().find()

    assert wagers.total == 1
    assert contests.total == 1
    assert contests.items[0].contest_uuid == contest_uuid
    assert contests.items[0].buy_in == buy_in
    assert payouts.total == 2
    for payout in payouts.items:
        assert payout.proportion in payout_list
    assert parties.total == 1
    assert participants.total == 1
    assert participants.items[0].member_uuid == member_uuid
    assert stakes.total == 1
    assert stakes.items[0].amount == buy_in


def test_contest_participant_active_async(get_contest_uuid):
    """
    GIVEN 1 wager instance, 1 contest instance, 2 payout instance, 1 party service, 1 participant service and 1 stake
    service instance in the database
    WHEN the CONTEST service notifies Kafka that an participant has been created
    THEN event contest handle_event participant_active adds 1 wager instance, 1 contest instance, 2 payout instance, 1 party
    service, 1 participant service and 1 stake service
    """
    contest_uuid = get_contest_uuid()
    member_uuid = generate_uuid()
    value = {
        'contest_uuid': str(contest_uuid),
        'participant_uuid': str(generate_uuid()),
        'member_uuid': str(member_uuid),
        'user_uuid': str(generate_uuid()),
        'owner_uuid': str(generate_uuid()),
        'league_uuid': str(generate_uuid()),
        'message': ''
    }

    base_service.notify(topic='contests', value=value, key='participant_active')
    time.sleep(0.5)

    wagers = services.WagerService().find()
    contests = services.ContestService().find()
    parties = services.PartyService().find()
    participants = services.ParticipantService().find()
    stakes = services.StakeService().find()

    assert wagers.total == 1
    assert contests.total == 1
    assert contests.items[0].contest_uuid == contest_uuid
    assert parties.total == 2
    assert participants.total == 2
    assert participants.items[0].member_uuid != participants.items[1].member_uuid
    assert stakes.total == 2
    assert stakes.items[0].amount == stakes.items[1].amount
