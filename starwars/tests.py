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

        assert persona.name == data[0]['name']
        assert persona.id == data[0]['id']
        assert persona.fraction.id == data[0]['fraction']['id']
        assert persona.race.id == data[0]['race']['id']
        assert persona.race.homePlanet.id == data[0]['race']['homePlanet']['id']

    def test_create_character(self):
        plnt = baker.make("Planet")
        frc = baker.make("Fraction")
        rc = baker.make("Race", homePlanet=plnt)

        r = self.client.post("/api/characters/", {
            "name" : "Лишний",
            "fraction" : frc.id,
            "race" : rc.id
        })

        new_character_id = r.json()['id']

        characters = Character.objects.all()
        assert len(characters) == 1

        new_character = Character.objects.filter(id=new_character_id).first()
        assert new_character.name == 'Лишний'
        assert new_character.fraction == frc
        assert new_character.race == rc

    def test_delete_person(self):
        characters = baker.make("Character", 10)
        r = self.client.get('/api/characters/')
        data = r.json()
        assert len(data) == 10

        character_id_to_delete = characters[3].id
        self.client.delete(f'/api/characters/{character_id_to_delete}/')

        r = self.client.get('/api/characters/')
        data = r.json()

        assert character_id_to_delete not in [i['id'] for i in data]

    def test_update_character(self):
        characters = baker.make("Character", 10)
        character : Character = characters[2]

        r = self.client.get(f'/api/characters/{character.id}/')
        data = r.json()
        assert data['name'] == character.name

        r = self.client.put(f'/api/characters/{character.id}/', {
            "name" : "Петр Петров"
        })
        assert r.status_code == 200
        
        r = self.client.get(f'/api/characters/{character.id}/')
        data = r.json()
        assert data['name'] == "Петр Петров"

        character.refresh_from_db()
        assert data['name'] == character.name

class PlanetsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        plnt = baker.make("Planet")

        r = self.client.get('/api/planets/')
        data = r.json()

        assert plnt.name == data[0]['name']
        assert plnt.id == data[0]['id']
        assert plnt.population == data[0]['population']

    def test_create_planet(self):
        r = self.client.post("/api/planets/", {
            "name" : "Лишний",
            "population" : "1"
        })

        new_planet_id = r.json()['id']

        planets = Planet.objects.all()
        assert len(planets) == 1

        new_planets = Planet.objects.filter(id=new_planet_id).first()
        assert new_planets.name == 'Лишний'
        assert new_planets.population == '1'

    def test_delete_planet(self):
        planets = baker.make("Planet", 10)
        r = self.client.get('/api/planets/')
        data = r.json()
        assert len(data) == 10

        planet_id_to_delete = planets[3].id
        self.client.delete(f'/api/planets/{planet_id_to_delete}/')

        r = self.client.get('/api/planets/')
        data = r.json()

        assert planet_id_to_delete not in [i['id'] for i in data]

    def test_update_planet(self):
        planets = baker.make("Planet", 10)
        planet : Planet = planets[2]

        r = self.client.get(f'/api/planets/{planet.id}/')
        data = r.json()
        assert data['name'] == planet.name

        r = self.client.put(f'/api/planets/{planet.id}/', {
            "name" : "Петр Петров",
            "population" : planet.population
        })
        assert r.status_code == 200
        
        r = self.client.get(f'/api/planets/{planet.id}/')
        data = r.json()
        assert data['name'] == "Петр Петров"

        planet.refresh_from_db()
        assert data['name'] == planet.name

class RacesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        plnt = baker.make("Planet")
        rc = baker.make("Race", homePlanet=plnt)

        r = self.client.get('/api/races/')
        data = r.json()

        assert rc.name == data[0]['name']
        assert rc.id == data[0]['id']
        assert rc.homePlanet.id == data[0]['homePlanet']['id']

    def test_create_race(self):
        plnt = baker.make("Planet")

        r = self.client.post("/api/races/", {
            "name" : "Лишний",
            "homePlanet" : plnt.id
        })

        new_race_id = r.json()['id']

        races = Race.objects.all()
        assert len(races) == 1

        new_race = Race.objects.filter(id=new_race_id).first()
        assert new_race.name == 'Лишний'
        assert new_race.homePlanet == plnt

    def test_delete_race(self):
        races = baker.make("Race", 10)
        r = self.client.get('/api/races/')
        data = r.json()
        assert len(data) == 10

        race_id_to_delete = races[3].id
        self.client.delete(f'/api/races/{race_id_to_delete}/')

        r = self.client.get('/api/races/')
        data = r.json()

        assert race_id_to_delete not in [i['id'] for i in data]

    def test_update_race(self):
        races = baker.make("Race", 10)
        race : Race = races[2]

        r = self.client.get(f'/api/races/{race.id}/')
        data = r.json()
        assert data['name'] == race.name

        r = self.client.put(f'/api/races/{race.id}/', {
            "name" : "Петр Петров"
        })
        assert r.status_code == 200
        
        r = self.client.get(f'/api/races/{race.id}/')
        data = r.json()
        assert data['name'] == "Петр Петров"

        race.refresh_from_db()
        assert data['name'] == race.name

class FractionsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        frc = baker.make("Fraction")

        r = self.client.get('/api/fractions/')
        data = r.json()

        assert frc.id == data[0]['id']
        assert frc.name == data[0]['name']
        assert frc.periodInLive == data[0]['periodInLive']

    def test_create_fraction(self):
        r = self.client.post("/api/fractions/", {
            "name" : "Лишний",
            "periodInLive" : "Как-то"
        })

        new_fraction_id = r.json()['id']

        fractions = Fraction.objects.all()
        assert len(fractions) == 1

        new_fraction = Fraction.objects.filter(id=new_fraction_id).first()

        assert new_fraction.id == new_fraction_id
        assert new_fraction.name == 'Лишний'
        assert new_fraction.periodInLive == 'Как-то'

    def test_delete_fraction(self):
        fractions = baker.make("Fraction", 10)
        r = self.client.get('/api/fractions/')
        data = r.json()
        assert len(data) == 10

        fraction_id_to_delete = fractions[3].id
        self.client.delete(f'/api/fractions/{fraction_id_to_delete}/')

        r = self.client.get('/api/fractions/')
        data = r.json()

        assert fraction_id_to_delete not in [i['id'] for i in data]

    def test_update_fraction(self):
        fractions = baker.make("Fraction", 10)
        fraction : Fraction = fractions[2]

        r = self.client.get(f'/api/fractions/{fraction.id}/')
        data = r.json()
        assert data['name'] == fraction.name

        r = self.client.put(f'/api/fractions/{fraction.id}/', {
            "name" : "Петр Петров",
            "periodInLive" : fraction.periodInLive
        })
        assert r.status_code == 200
        
        r = self.client.get(f'/api/fractions/{fraction.id}/')
        data = r.json()
        assert data['name'] == "Петр Петров"

        fraction.refresh_from_db()
        assert data['name'] == fraction.name

class StarShipsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        star_ship = baker.make("Starship")

        r = self.client.get('/api/starships/')
        data = r.json()

        assert star_ship.name == data[0]['name']
        assert star_ship.crew == data[0]['crew']
        assert star_ship.type == data[0]['type']
        assert star_ship.id == data[0]['id']

    def test_create_starshp(self):
        r = self.client.post("/api/starships/", {
            "name" : "Лишний",
            "type" : "Какой-то",
            "crew" : "Кто-то"
        })

        new_star_ship_id = r.json()['id']

        star_ships = Starship.objects.all()
        assert len(star_ships) == 1

        new_star_ship = Starship.objects.filter(id=new_star_ship_id).first()
        assert new_star_ship.name == 'Лишний'
        assert new_star_ship.crew == "Кто-то"
        assert new_star_ship.type == "Какой-то"

    def test_delete_starship(self):
        star_ships = baker.make("Starship", 10)
        r = self.client.get('/api/starships/')
        data = r.json()
        assert len(data) == 10

        star_ship_id_to_delete = star_ships[3].id
        self.client.delete(f'/api/starships/{star_ship_id_to_delete}/')

        r = self.client.get('/api/starships/')
        data = r.json()

        assert star_ship_id_to_delete not in [i['id'] for i in data]

    def test_update_starship(self):
        star_ships = baker.make("Starship", 10)
        star_ship : Starship = star_ships[2]

        r = self.client.get(f'/api/starships/{star_ship.id}/')
        data = r.json()
        assert data['name'] == star_ship.name

        r = self.client.put(f'/api/starships/{star_ship.id}/', {
            "name" : "Петр Петров",
            "type" : star_ship.type,
            "crew" : star_ship.crew
        })
        assert r.status_code == 200
        
        r = self.client.get(f'/api/starships/{star_ship.id}/')
        data = r.json()
        assert data['name'] == "Петр Петров"

        star_ship.refresh_from_db()
        assert data['name'] == star_ship.name