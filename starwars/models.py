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

class Jedi(models.Model):
    name = models.TextField("Имя")
    padavan = models.TextField("Падаван")
    race = models.ForeignKey("Race", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Джедай"
        verbose_name_plural = "Джедаи"