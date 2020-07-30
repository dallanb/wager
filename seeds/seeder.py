import random
from flask import g
from flask_seeder import Seeder
from src.common import generate_uuid, time_now
from src.services import Wager, Course
import logging


# All seeders inherit from Seeder
class DefaultSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    @staticmethod
    def run():
        g.user = generate_uuid()
        courses = Course.find_course_by_golf_canada_id(golf_canada_id=18946)  # Gleneagles

        for _ in range(5):
            members = [generate_uuid() for _ in range(3)]
            currency = 'CAD'
            amount = random.randint(0, 100)
            time = time_now()
            course = courses[0]

            Wager.create_wager(members=members, currency=currency, amount=amount, time=time, course=course)
