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

        for _ in range(5):
            wager = services.init_wager(owner_uuid=g.user, status='pending')

            services.save_wager(wager=wager)
