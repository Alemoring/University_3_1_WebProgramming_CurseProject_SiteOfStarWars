from django.db import models

# Create your models here.
class Race(models.Model):
    name = models.TextField("Название")
    homePlanet = models.TextField("Родная планета")
    class Meta:
        verbose_name = "Расса"
        verbose_name_plural = "Рассы"
    def __str__(self) -> str:
        return self.name

class Character(models.Model):
    name = models.TextField("Имя")
    fraction = models.TextField("Фракция")
    race = models.ForeignKey("Race", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"