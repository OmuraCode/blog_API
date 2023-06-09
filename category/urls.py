from django.urls import path

from category import views

urlpatterns = [
    path('', views.CategoryCreateListView.as_view()),
]