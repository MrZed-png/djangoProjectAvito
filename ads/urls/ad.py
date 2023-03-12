from django.urls import path

from ads import views

urlpatterns = [
    path('<int:pk>/', views.AdDetailView.as_view()),
    path('<int:pk>/image/', views.AdUploadImageView.as_view()),
    path('<int:pk>/delete/', views.AdDeleteView.as_view()),
    path('<int:pk>/update/', views.AdUpdateView.as_view()),
    path('', views.AdListView.as_view())
]
