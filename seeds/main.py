import random
from flask import g
from flask_seeder import Seeder
from src.common import generate_uuid, time_now
from src import services


# All seeders inherit from Seeder
class DefaultSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    @staticmethod
    def run():
        g.user = generate_uuid()
        course = services.find_course_by_golf_canada_id(golf_canada_id=18946)  # Gleneagles
        status = services.find_wager_status_by_enum('active')

        for _ in range(5):
            members = [generate_uuid() for _ in range(3)]
            party = services.init_party_by_members(members=members)
            stake = services.init_stake(currency='CAD', amount=random.randint(0, 100))
            wager = services.init_wager(owner=g.user, party=party, stake=stake, time=time_now(), course=course,
                                        status=status)
            services.save_wager(wager=wager)
