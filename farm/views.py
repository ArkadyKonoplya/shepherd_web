from datetime import datetime, timedelta
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View

from field.views import generate_location_weather
from farm.models import Farm, FarmUsers
from farm.forms import FarmForm
from field.models import Location
from task.models import Task, TaskHistory
from work_order.models import WorkOrder

from .forms import FarmForm


class ProfileView(generic.UpdateView):
    model = Farm
    form_class = FarmForm
    success_url = reverse_lazy("farm_profile")
    template_name = "farm/profile.html"

    def get(self, request, *args, **kwargs):
        farm = kwargs.get('pk', None)

        if 'weather' in request.session.keys():
            weather_info = request.session['weather']
        else:
            generate_location_weather(request)
            weather_info = request.session['weather']

        if farm is None:
            farm = Farm.objects.get(member_farms__user_id=request.user.id, member_farms__default_farm=True)
            farm = farm.id

        farm = get_object_or_404(Farm, id=farm)
        form = self.form_class(request=request)

        farm_members = FarmUsers.objects.select_related("user", "role").filter(farm__id=farm.id).order_by("role__name")
        farm_members_count = farm_members.count()
        tasks = TaskHistory.objects.select_related("task_status", "task_id", "task_id__task_plan__crop", "task_id__task_activity", "task_id__task_plan__location", "update_user").filter(task_id__task_plan__location__location_farms__farm__id=farm.id).order_by("-status_date_change")[:5]

        return render(request, self.template_name, {"form": form, "farm": farm, "tasks": tasks, "farm_members": farm_members, "farm_members_count": farm_members_count, "weather": weather_info[str(farm.main_location.id)]})


@login_required
def farm_details(request):
    """
    Main page for working on the farm object.
    :param request:
    :return:
    """

    farm_instance = get_object_or_404(Farm, pk=request.session["farm"])
    form = FarmForm(request.POST or None, instance=farm_instance, request=request)

    if form.is_valid():
        farm = form.save(commit=False)
        farm.modified_at = datetime.now()
        farm.modified_by = request.user.id
        farm.save()

    return render(
        request, "farm/farm_detail.html", {"form": form}
    )

@login_required
def farm_dashboard(request):
    """
    Main login page for users.
    :param request:
    :return:
    """
    if 'weather' in request.session.keys():
        weather_info = request.session['weather']
    else:
        generate_location_weather(request)
        weather_info = request.session['weather']

    if "farm" not in request.session:
        farm = Farm.objects.get(
            member_farms__default_farm=True, member_farms__user_id=request.user.id
        )
        request.session["farm"] = str(farm.id)

    try:
        default_location = Farm.objects.get(pk=request.session["farm"])
        default_location = default_location.main_location.geo_center
    except:
        default_location = [-99.83071945037129, 40.62995241492818]

    today = datetime.today()
    yesterday = today - timedelta(days=1)

    overdue_tasks = (
        Task.objects.select_related("task_plan__location")
        .filter(
            task_plan__location__location_farms__farm__member_farms__user_id=request.user.id
        )
        .filter(task_status__name__in=("accepted", "available", "assigned", "declined"))
        .filter(task_end_date__lt=today)
    )
    overdue_tasks_count = overdue_tasks.count()
    overdue_tasks = overdue_tasks.order_by("-task_end_date")[:5]

    in_progress_tasks = (
        Task.objects.select_related("task_plan__location")
        .filter(
            task_plan__location__location_farms__farm__member_farms__user_id=request.user.id
        )
        .filter(task_status__name="accepted")
        .filter(task_end_date__gte=today)
    )

    task_weather = dict()

    for task in overdue_tasks:

        location = str(task.task_plan.location.id)
        task_weather[task.id] = weather_info[location]

    in_progress_tasks_count = in_progress_tasks.count()
    in_progress_tasks = in_progress_tasks.order_by("task_end_date")[:5]

    for task in in_progress_tasks:

        location = task.task_plan.location.id
        try:
            task_weather[task.id] = weather_info[location]
        except KeyError:
            pass

    updated_tasks = TaskHistory.objects.select_related(
        "task_id",
        "update_user",
        "task_status",
        "task_id__task_plan__location",
        "task_id__task_plan__crop",
    ).filter(
        status_date_change__gte=yesterday,
        task_id__task_plan__location__location_farms__farm_id=request.session["farm"]
    ).order_by("task_id", "-status_date_change").distinct("task_id")

    overdue_work_orders = WorkOrder.objects.filter(
        farm__id=request.session["farm"]
    ).filter(end_date__lt=today)
    overdue_work_orders_count = overdue_work_orders.count()
    overdue_work_orders = overdue_work_orders.order_by("-end_date")[:5]

    in_progress_work_orders = WorkOrder.objects.filter(
        farm__id=request.session["farm"]
    ).filter(end_date__lt=today)
    in_progress_work_orders_count = in_progress_work_orders.count()
    in_progress_work_orders = in_progress_work_orders.order_by("end_date")[:5]

    return render(
        request,
        "dashboard.html",
        {
            "in_progress_tasks": in_progress_tasks,
            "in_progress_tasks_count": in_progress_tasks_count,
            "in_progress_work_orders": in_progress_work_orders,
            "in_progress_work_orders_count": in_progress_work_orders_count,
            "overdue_tasks": overdue_tasks,
            "overdue_tasks_count": overdue_tasks_count,
            "overdue_work_orders": overdue_work_orders,
            "overdue_work_orders_count": overdue_work_orders_count,
            "task_weather": task_weather,
            "google_key": os.getenv("google_maps_api_key"),
            "map_center_lat": default_location[1],
            "map_center_lng": default_location[0],
            "updated_tasks": updated_tasks,
        },
    )
