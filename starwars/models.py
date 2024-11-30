from django.db import models

# Create your models here.
class Fraction(models.Model):
    name = models.TextField("Название")
    periodInLive = models.TextField("Период существования")

    class Meta:
        verbose_name = "Фракция"
        verbose_name_plural = "Фракции"
    def __str__(self) -> str:
        return self.name

class Planet(models.Model):
    name = models.TextField("Название")
    population = models.TextField("Популяция")

    class Meta:
        verbose_name = "Планета"
        verbose_name_plural = "Планеты"
    def __str__(self) -> str:
        return self.name

class Race(models.Model):
    name = models.TextField("Название")
    homePlanet = models.ForeignKey("Planet", on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name = "Расса"
        verbose_name_plural = "Рассы"
    def __str__(self) -> str:
        return self.name

class Character(models.Model):
    name = models.TextField("Имя")
    fraction = models.ForeignKey("Fraction", on_delete=models.CASCADE, null=True)
    race = models.ForeignKey("Race", on_delete=models.CASCADE, null=True)

    picture = models.ImageField("Изображение", null = True, upload_to="characters")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

class Starship(models.Model):
    name = models.TextField("Название")
    type = models.TextField("Тип корабля")
    crew = models.TextField("Экипаж корабля")
    picture = models.ImageField("Изображение", null = True, upload_to="starships")

    class Meta:
        verbose_name = "Звёздный корабль"
        verbose_name_plural = "Звёздные корабли"