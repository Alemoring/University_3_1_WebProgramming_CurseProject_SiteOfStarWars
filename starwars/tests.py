from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from starwars.models import Planet, Fraction, Character, Race, Starship

# Create your tests here.
class CharactersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        plnt = baker.make("Planet")
        frc = baker.make("Fraction")
        rc = baker.make("Race", homePlanet=plnt)
        persona = baker.make("Character", fraction=frc, race=rc)

        r = self.client.get('/api/characters/')
        data = r.json()
        print(data)

        assert persona.name == data[0]['name']
        assert persona.id == data[0]['id']
        assert persona.fraction.id == data[0]['fraction']['id']
        assert persona.race.id == data[0]['race']['id']
        assert persona.race.homePlanet.id == data[0]['race']['homePlanet']['id']

    def test_create_character(self):
        plnt = Planet.objects.create(
            name = "Лишний",
            population = "1 000 000 000 000"
        )
        frc = Fraction.objects.create(
            name = "Лишний",
            periodInLive = "25 025 ДБЯ - По наши дни"
        )
        rc = Race.objects.create(
            name = "Лишний",
            homePlanet = plnt
        )
        r = self.client.post("/api/characters/", {
            "name" : "Лишний",
            "fraction" : frc.id,
            "race" : rc.id
        })

        new_character_id = r.json()['id']

        characters = Character.objects.all()
        assert len(characters) == 1

        new_character = Character.objects.filter(id=new_character_id).first()
        print(new_character.fraction)
        assert new_character.name == 'Лишний'
        assert new_character.fraction == frc
        assert new_character.race == rc

    