from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=300)
    is_published = models.BooleanField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
