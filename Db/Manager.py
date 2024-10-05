import peewee
from Db.Models import Fixture

class DbManager:

    def __init__(self):
        try:
            self.fixture = Fixture(fixture_id="HR001", fail_count=0, steps_count=0, online=True)
            self.fixture.save()
        except peewee.IntegrityError:
            print("No")