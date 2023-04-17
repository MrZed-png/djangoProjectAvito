from django.urls import path
from rest_framework.routers import SimpleRouter

from ads import views
from ads.views import AdsViewSet

router = SimpleRouter()
router.register('', AdsViewSet)

urlpatterns = [

    path('<int:pk>/upload_image/', views.AdsUploadImageView.as_view(), name='ads_upload_image'),

    ]

urlpatterns += router.urls