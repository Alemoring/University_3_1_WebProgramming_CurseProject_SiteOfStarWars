from rest_framework import serializers

from starwars.models import Character, Race

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"

class CharacterSerializer(serializers.ModelSerializer):
    race = RaceSerializer(read_only=True)
    class Meta:
        model = Character
        fields = ['id', 'name', 'race']