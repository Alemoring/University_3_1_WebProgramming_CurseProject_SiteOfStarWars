from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from starwars.models import Planet, Fraction, Character, Race, Starship

# Create your tests here.
class CharactersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        plnt = Planet.objects.create(
            name = "Корусант",
            population = "1 000 000 000 000"
        )
        frc = Fraction.objects.create(
            name = "Джедаи",
            periodInLive = ""
        )
        rc = 
        r = self.client.get('/api/starwars/')
        print(r)