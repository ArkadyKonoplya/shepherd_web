from django.urls import path
from django.conf.urls import url
from django import views as django_views

from .views import equipment_list, equipment_create, equipment_detail, ProfileView

urlpatterns = [
    path("", equipment_list, name="equipment_list"),
    path("new", equipment_create, name="equipment_create"),
    path("<uuid:pk>", equipment_detail, name="equipment_detail"),
    path("profile/<str:pk>/", ProfileView.as_view(), name="equipment_profile"),
]
