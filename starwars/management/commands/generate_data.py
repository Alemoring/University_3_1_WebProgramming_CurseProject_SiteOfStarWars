from django.core.management.base import BaseCommand

from faker import Faker
import random

from django.contrib.auth.models import User
from starwars.models import Planet, Fraction, Race, Starship

users = User.objects.all()
#print(users[random.randint(0, 1)])
class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        # for _ in range(975):
            # Planet.objects.create(
            #     name=fake.name(),
            #     population = str(random.randint(1000000, 310000005))
            # )
            # Fraction.objects.create(
            #      name=fake.name(),
            #      periodInLive = str(random.randint(1000000, 310000005))
            #  )
            # Starship.objects.create(
            #       name=fake.name(),
            #       type = fake.word(),
            #       crew = fake.sentence(),
            #       user = users[random.randint(0, 1)]
            #   )