from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.name


class User(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'Admin', 'Админ'
        MEMBER = 'Member', 'Пользователь'
        MODERATOR = 'Moderator', 'Модератор'

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=Roles.choices)
    age = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
