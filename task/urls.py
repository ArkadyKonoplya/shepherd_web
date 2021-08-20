from django.urls import path
from django.conf.urls import url
from django import views as django_views

from .views import (
    calender_view,
    in_progress_task_list,
    overdue_task_list,
    task_create,
    task_detail,
    task_list,
    task_reassign,
    worker_view,
)

urlpatterns = [
    path("", task_list, name="task_list"),
    path("calendar/", calender_view, name="calendar"),
    path("worker/", worker_view, name="worker_view"),
    path("overdue/", overdue_task_list, name="overdue_tasks"),
    path("in-progress/", in_progress_task_list, name="in_progress_tasks"),
    path("task/<uuid:pk>", task_detail, name="task_detail"),
    path("task/new", task_create, name="task_create"),
    path(
        "task/reassign/<uuid:pk>/<uuid:assignee>", task_reassign, name="task_reassign"
    ),
    url(r"^jsi18n/$", django_views.i18n.JavaScriptCatalog.as_view(), name="jsi18n"),
]
