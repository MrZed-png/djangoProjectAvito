from django.db.models import Count, Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


from djangoProject_27.serializers import UserSerializer, UserListSerializer, UserDetailSerializer, LocationSerializer, \
    UserCreateSerializer
from users.models import User, Location


#пишем свой пагинатор для юзеров
class UserPagination(PageNumberPagination):
    page_size = 4


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDeleteView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.annotate(total_ads =Count("ads", filter = Q(ads__is_published=True))).order_by() #аннотация - это поле будет добавляться в queryset из запроса
    #queryset = User.objects.all().order_by("username") - это для худшегь варианта подсчета исла заявлений
    pagination_class = UserPagination


class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()