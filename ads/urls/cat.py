from django.urls import path

from ads import views
from ads.views import CategoryListView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('create/', views.CategoryCreateView.as_view()),
    path('<int:pk>/update/', views.CategoryUpdateView.as_view()),
    path('<int:pk>/', views.CategoryDetailView.as_view()),
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view())
]
