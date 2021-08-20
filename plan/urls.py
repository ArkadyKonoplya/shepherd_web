from django.urls import path
from django.conf.urls import url
from django import views as django_views

from .views import plan_list, plan_create, plan_detail

urlpatterns = [
    path("", plan_list, name="plan_list"),
    path("new", plan_create, name="plan_create"),
    path("<uuid:pk>", plan_detail, name="plan_detail"),
]