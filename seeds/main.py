from flask_seeder import Seeder

from src import services


# All seeders inherit from Seeder
class DefaultSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    @staticmethod
    def run():
        base = services.Base()
        # for _ in range(20):
        #     wager = base.init(model=models.Wager, status='pending')
        #     wager = base.save(instance=wager)
        #     for _ in range(2):
        #         party = base.init(model=models.Party,
        #                           name=''.join(random.choice(string.ascii_letters) for i in range(10)),
        #                           wager=wager)
        #         party = base.save(instance=party)
        #         for _ in range(2):
        #             participant = base.init(model=models.Participant, user_uuid=generate_uuid(),
        #                                     status='pending', party=party)
        #             participant = base.save(instance=participant)
        #             for _ in range(1):
        #                 stake = base.init(model=models.Stake, amount=random.randint(1, 100),
        #                                   participant=participant)
        #                 _ = base.save(instance=stake)
