from rest_framework import serializers

from starwars.models import Character, Planet, Race, Starship, Fraction

class FractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fraction
        fields = "__all__"

class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = "__all__"

class RaceSerializer(serializers.ModelSerializer):
    homePlanet = PlanetSerializer(read_only=True)
    class Meta:
        model = Race
        fields = "__all__"
class RaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"

class CharacterSerializer(serializers.ModelSerializer):
    race = RaceSerializer(read_only=True)
    fraction = FractionSerializer(read_only=True)
    class Meta:
        model = Character
        fields = "__all__"

class CharacterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"

class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = "__all__"
class StarshipDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = "__all__"