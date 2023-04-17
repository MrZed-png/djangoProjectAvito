from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from ads.models import Category, Ads, Selection
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdsSerializer, AdsDetailSerializer, AdsListSerializer, SelectionSerializer, \
    SelectionCreateSerializer, CategorySerializer


class CatViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdsViewSet(ModelViewSet):
    default_serizalizer = AdsSerializer
    queryset = Ads.objects.order_by('-price')
    serializers = {'retrieve': AdsDetailSerializer,
                   'list': AdsListSerializer
                   }
    default_permission = [AllowAny]
    permissions = {"retrieve": [IsAuthenticated],
                   'update': [IsAuthenticated, IsOwner | IsStaff],
                   'partial_update': [IsAuthenticated, IsOwner | IsStaff],
                   'destroy': [IsAuthenticated, IsOwner | IsStaff]
                   }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    # то есть получаем список из словаря, если есть на это action, сработает, если нет - возьмется дефортный

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serizalizer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)  # переопределяем queryset

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)  # переопределяем queryset

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(
                author_id__location__name__icontains=location)  # переопределяем queryset

        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)  # переопределяем queryset

        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)  # переопределяем queryset

        return super().list(request, *args, **kwargs)


class SelectionViewSet(ModelViewSet):
    serializer_class = SelectionSerializer
    queryset = Selection.objects.all()
    default_permission = [AllowAny]
    permissions = {"create": [IsAuthenticated],
                   "update": [IsAuthenticated, IsOwner],
                   "partial_update": [IsAuthenticated, IsOwner],
                   "destroy": [IsAuthenticated, IsOwner]}

    default_serializer = SelectionSerializer
    serializers = {"create": SelectionCreateSerializer,
                   }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUploadImageView(generic.UpdateView):
    model = Ads
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image')
        self.object.save()

        result = serialize(self.model, self.object)
        return JsonResponse(result, safe=False)


def serialize(model, values):  # model:<class 'ads.models.Category>' values:Class
    if isinstance(values, model):
        values = [values]
    else:
        list(values)

    result = []
    for value in values:  # value: Category object (1)
        data = {}
        for field in model._meta.get_fields():
            if field.is_relation:
                continue
            if field.name == 'image':
                data[field.name] = getattr(value.image, 'url', None)
            else:
                data[field.name] = getattr(value, field.name)
        result.append(data)

    return result
