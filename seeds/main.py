import random
import string
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

        for _ in range(20):
            wager = services.init_wager(owner_uuid=g.user, status='pending')
            wager = services.save_wager(wager=wager)
            party = services.init_party(name=''.join(random.choice(string.ascii_letters) for i in range(10)),
                                        wager=wager)
            party = services.save_party(party=party)
            for _ in range(2):
                participant = services.init_participant(user_uuid=generate_uuid(), status='pending', party=party)
                participant = services.save_participant(participant=participant)
