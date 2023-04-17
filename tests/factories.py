import factory.django

from ads.models import Category, Ads
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Faker("name")


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("ean")


class AdFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Ads

    name = factory.Faker("name")
    category_id = factory.SubFactory(CategoryFactory)
    author_id = factory.SubFactory(UserFactory)
    price = 200
