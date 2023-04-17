from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import LocationViewSet

router = SimpleRouter()
router.register('location', LocationViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('cat/', include('ads.urls.categories')),
    path('ads/', include ('ads.urls.ads')),
    path('selection/', include ('ads.urls.selections')),
    path('user/', include('users.urls')),

]

urlpatterns += router.urls