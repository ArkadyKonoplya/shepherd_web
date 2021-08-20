from django.urls import path
from django.conf.urls import url
from django import views as django_views

from .views import (
    work_order_create,
    work_order_detail,
    work_order_list,
    overdue_work_orders,
    in_progress_work_orders,
)

urlpatterns = [
    path("", work_order_list, name="work_order_list"),
    path("work_order/<uuid:pk>", work_order_detail, name="work_order_detail"),
    path("work_order/new", work_order_create, name="work_order_create"),
    path("overdue/", overdue_work_orders, name="overdue_work_orders"),
    path("in-progress/", in_progress_work_orders, name="in_progress_work_orders"),
]
