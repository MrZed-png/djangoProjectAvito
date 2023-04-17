from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserCreateSerializer(ModelSerializer):
    location = SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field="name"
    )

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        password = validated_data.pop('password')
        new_user = User.objects.create(**validated_data)
        new_user.set_password(password)
        new_user.save()

        for loc in self._location:
            location, _ = Location.objects.get_or_create(name=loc)
            new_user.location.add(location)
        return new_user

    class Meta:
        model = User
        fields = '__all__'


    class Meta:
        model = User
        fields = "__all__"

class UserListSerializer(ModelSerializer):
    total_ads = IntegerField()

    #вариант старый - хуже
    #total_ads = SerializerMethodField()

    #def get_total_ads(self, user): #обязательно, чтобы функция содержала get, нижнее подчеркивание, название поля
    #принимает объект из базы, то есть кому мы добавляем поле
        #return user.ads_set.filter(is_published = True).count()
    #ads_set - это обратное обращение к моделям

    class Meta:
        model = User
        fields = ['username', 'total_ads']

class UserDetailSerializer(ModelSerializer):
    location = SlugRelatedField(queryset=Location.objects.all(), slug_field = "name", many=True) #мз всех локаций выбараем соответствующую локацию и выводим name локации

    class Meta:
        model = User
        exclude = ['password']

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

