from django.urls import path
from django.conf.urls import url
from django import views as django_views

from .views import location_list, location_detail, location_create, ProfileView

urlpatterns = [
    path("", location_list, name="location_list"),
    path("location/<uuid:pk>", location_detail, name="location_detail"),
    path("location/new", location_create, name="location_create"),
    path("profile/<str:pk>/", ProfileView.as_view(), name="location_profile"),
]
