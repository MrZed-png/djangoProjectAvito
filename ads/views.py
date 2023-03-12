import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from homework27 import settings


def root(request):
    return JsonResponse({"status": "ok"})


def serialize(model, values):
    if isinstance(values, model):
        values = [values]
    else:
        list(values)

    result = []

    for value in values:
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


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_name = request.GET.get("name", None)
        if search_name:
            self.object_list = self.object_list.filter(name=search_name)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_odj = paginator.get_page(page_number)

        categories = []
        for category in page_odj:
            categories.append({
                "id": category.id,
                "name": category.name,
            })

        response = {
            "items": categories,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data['name']

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data['name']
        )
        category.save()

        return JsonResponse({
            "id": category.id,
            "text": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ads = self.get_object()
        result = serialize(Ad, ads)

        return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "image"]

    def post(self, request):
        self.object = self.get_object()
        ads = self.object

        ads.image = request.FILES['image']
        ads.save()
        result = serialize(Ad, ads)

        return JsonResponse(result, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'address', 'is_published']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.id = ad_data['id']
        self.object.name = ad_data['name']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.address = ad_data['address']
        self.object.save()

        result = serialize(Ad, ad_data)

        return JsonResponse(result, safe=False)


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("author_id")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_odj = paginator.get_page(page_number)
        ads = serialize(Ad, page_odj)

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)
