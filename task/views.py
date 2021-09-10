import json
from datetime import datetime
import os

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from fcm_django.models import FCMDevice

from .models import Task, TaskStatus

from .forms import TaskForm

from field.views import generate_location_weather
from farm.models import Farm
from user.models import ShepherdUser
from work_order.models import WorkOrder


@login_required
def task_reassign(request, pk, assignee):
    task = Task.objects.get(pk=pk)
    task.task_assignee = assignee
    task.task_status = TaskStatus.objects.get(name="assigned")
    task.save()

    create_notification(action="update", task=task, request=request)

    return True


@login_required
def task_create(request):
    # context = {}

    # form = TaskForm(request.POST or None, request=request)
    # if form.is_valid():
    #     task = form.save(commit=False)
    #     task.task_creator = request.user

    #     if not task.task_assignee:
    #         task.task_status = TaskStatus.objects.get(name="available")
    #     else:
    #         task.task_status = TaskStatus.objects.get(name="assigned")

    #     task.save()

    #     messages.add_message(
    #         request, messages.SUCCESS, "Task was created successfully!"
    #     )

    #     create_notification(action="create", task=task, request=request)

    #     return redirect("task_detail", uuid=task.id)
    # else:
    #     messages.add_message(request, messages.ERROR, form.errors)

    # context["form"] = form
    # return render(request, "tasks/create_task.html", context)
    return render(request, "tasks/create_task.html")


@login_required
def task_detail(request, pk):
    if 'weather' not in request.session.keys():
        generate_location_weather(request)

    task_instance = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task_instance, request=request)

    if form.is_valid():
        task = form.save(commit=False)
        task.modified_at = datetime.now()
        task.modified_by = request.user.id
        task.save()

        if task.task_status == TaskStatus.objects.get(name="completed"):
            work_order = WorkOrder.objects.get(task_work_orders__task=task)
            if work_order:
                work_order.tasks_completed = work_order.tasks_completed + 1
                work_order.save()

        create_notification(action="update", task=task, request=request)

        return redirect("task_detail", pk=task_instance.id)
    return render(
        request, "tasks/update_task.html", {"form": form, "uuid": task_instance.id, "location_weather": request.session['weather'][str(task_instance.task_plan.location.id)]}
    )


@login_required
def in_progress_task_list(request):
    today = datetime.today()
    tasks = (
        Task.objects.select_related(
            "task_creator",
            "task_plan__location",
            "task_status",
            "task_plan__crop",
        )
            .filter(
            task_plan__location__location_farms__farm__member_farms__user_id=request.user.id
        )
            .filter(task_status__name="accepted")
            .filter(task_end_date__gte=today)
    )

    weather_info = generate_task_weather(request.user.id, tasks)

    task_counts = (
        Task.objects.select_related("task_status")
            .values("task_status__name")
            .filter(task_plan__location__farm__member_farms__user__id=request.user.id)
            .annotate(count=Count("task_status"))
            .filter(task_start_date__year__gte=today.year)
    )

    open_tasks = 0
    in_process_tasks = 0
    completed_tasks = 0

    for count in task_counts:
        if count["task_status__name"] in ("assigned", "declined"):
            open_tasks += count["count"]

        if count["task_status__name"] in ("accepted"):
            in_process_tasks += count["count"]

        if count["task_status__name"] in ("archived", "completed"):
            completed_tasks += count["count"]

    table_title = "In Progress Tasks"

    return render(
        request,
        "tasks/tasks.html",
        {
            "tasks": tasks,
            "open_tasks": open_tasks,
            "in_process_tasks": in_process_tasks,
            "completed_tasks": completed_tasks,
            "table_title": table_title,
            "task_weather": weather_info["task_weather"],
            "task_historical_weather": weather_info["task_historical_weather"],
        },
    )


@login_required
def overdue_task_list(request):
    today = datetime.today()
    tasks = (
        Task.objects.select_related(
            "task_creator",
            "task_plan__location",
            "task_status",
            "task_plan__crop",
        )
            .filter(
            task_plan__location__location_farms__farm__member_farms__user_id=request.user.id
        )
            .filter(task_status__name__in=("accepted", "available", "assigned", "declined"))
            .filter(task_end_date__lt=today)
    )

    weather_info = generate_task_weather(request.user.id, tasks)

    task_counts = (
        Task.objects.select_related("task_status")
            .values("task_status__name")
            .filter(task_plan__location__farm__member_farms__user__id=request.user.id)
            .annotate(count=Count("task_status"))
            .filter(task_start_date__year__gte=today.year)
    )

    open_tasks = 0
    in_process_tasks = 0
    completed_tasks = 0

    for count in task_counts:
        if count["task_status__name"] in ("assigned", "declined"):
            open_tasks += count["count"]

        if count["task_status__name"] in ("accepted"):
            in_process_tasks += count["count"]

        if count["task_status__name"] in ("archived", "declined"):
            completed_tasks += count["count"]

    table_title = "Overdue Tasks"

    return render(
        request,
        "tasks/tasks.html",
        {
            "tasks": tasks,
            "open_tasks": open_tasks,
            "in_process_tasks": in_process_tasks,
            "completed_tasks": completed_tasks,
            "table_title": table_title,
            "task_weather": weather_info["task_weather"],
            "task_historical_weather": weather_info["task_historical_weather"],
        },
    )


@login_required
def task_list(request):
    # today = datetime.now()
    # tasks = generate_task_list(request.user.id)

    # weather_info = generate_task_weather(request, tasks)

    # task_counts = (
    #     Task.objects.select_related("task_status")
    #         .values("task_status__name")
    #         .filter(task_plan__location__farm__member_farms__user__id=request.user.id)
    #         .annotate(count=Count("task_status"))
    #         .filter(task_start_date__year__gte=today.year)
    # )

    # open_tasks = 0
    # in_process_tasks = 0
    # completed_tasks = 0

    # for count in task_counts:
    #     if count["task_status__name"] in ("assigned", "declined"):
    #         open_tasks += count["count"]

    #     if count["task_status__name"] in ("accepted"):
    #         in_process_tasks += count["count"]

    #     if count["task_status__name"] in ("archived", "declined"):
    #         completed_tasks += count["count"]

    # table_title = "Recent Tasks"

    # return render(
    #     request,
    #     "tasks/tasks.html",
    #     {
    #         "tasks": tasks,
    #         "open_tasks": open_tasks,
    #         "in_process_tasks": in_process_tasks,
    #         "completed_tasks": completed_tasks,
    #         "table_title": table_title,
    #         "task_weather": weather_info
    #     },
    # )
    return render(request, "tasks/tasks.html")


@login_required
def calender_view(request):
    # tasks = generate_calendar_task_list(request.user.id)
    # form = TaskForm(request.POST or None, request=request)

    # if form.is_valid():
    #     task = form.save(commit=False)
    #     task.task_creator = request.user
    #     task.task_status = TaskStatus.objects.get(name="assigned")
    #     task.save()
    #     form = TaskForm(request=request)
    # else:
    #     messages.add_message(request, messages.ERROR, form.errors)

    # return render(request, "tasks/calendar.html", {"tasks": tasks, "form": form})
    return render(request, "tasks/calendar.html")


@login_required
def worker_view(request):
    # tasks = generate_kanban_task_list(request.user.id)

    # return render(request, "tasks/workers.html", {"tasks": tasks})
    return render(request, "tasks/workers.html")


def determine_task_color(status, start_date, end_date):
    """
    For the calendar, determine what color the task should be
    :param status: The task's current status
    :param start_date: The task's start date
    :param end_date: The task's end date
    :return: str The calendar color class
    """

    today = datetime.now()

    if end_date.date() < today.date() and status not in (
            "completed",
            "archived",
            "deleted",
    ):
        return "bg-soft-danger"

    if (
            end_date.date() == today.date()
            and status not in ("completed", "archived", "deleted")
    ) or status == "declined":
        return "bg-soft-warning"

    if status in ("completed", "archived", "deleted"):
        return "bg-soft-light"

    if status == "assigned":
        return "bg-soft-primary"

    return "bg-soft-primary"


def generate_task_list(user_id):
    """
    Based on the user id, get the list of tasks for the given farm for the tasks page.
    :param user_id:
    :return:
    """
    today = datetime.now()
    tasks = (
        Task.objects.select_related(
            "task_creator",
            "task_plan__location",
            "task_status",
            "task_plan__crop",
        )
            .filter(task_plan__location__farm__member_farms__user__id=user_id)
            .filter(task_start_date__year__gte=today.year)
    )

    return tasks


def generate_calendar_task_list(user_id):
    """
    Based on the user id, get the list of tasks for the given farm(s) for the calendar page.
    :param user_id:
    :return:
    """
    tasks = Task.objects.select_related(
        "task_creator",
        "task_assignee",
        "task_plan__location",
        "task_status",
        "task_plan__crop",
    ).filter(task_plan__location__farm__member_farms__user__id=user_id)

    task_list = list()

    for task in tasks:

        task_color = determine_task_color(
            task.task_status.name, task.task_start_date, task.task_end_date
        )

        task_list.append(
            {
                "id": task.id,
                "title": f"{task.get_activity_name()} {task.task_plan.crop.name} in {task.task_plan.location.name}",
                "start": datetime.strftime(task.task_start_date, "%Y-%m-%d"),
                "end": datetime.strftime(task.task_end_date, "%Y-%m-%d"),
                "description": task.task_notes,
                "className": task_color,
                "location": task.task_plan.location.name,
                "organizer": f"{task.task_creator.first_name} {task.task_creator.last_name}",
                "worker": f"{task.task_assignee.first_name} {task.task_assignee.last_name}",
            }
        )

    return json.dumps(task_list, default=str)


def generate_kanban_task_list(user_id):
    """
    Based on the user id, get the list of tasks for the given farm(s) for the kanban worker page.
    :param user_id:
    :return:
    """
    user_farms = Farm.objects.filter(member_farms__user_id=user_id) | Farm.objects.filter(child_farm__parent_org__member_farms__user_id=user_id)

    tasks = (
        Task.objects.select_related(
            "task_creator",
            "task_assignee",
            "task_plan__location",
            "task_status",
            "task_plan__crop",
        )
            .filter(task_plan__location__farm__in=user_farms) \
            .filter(task_status__name__in=("accepted", "assigned", "available", "declined"))
            .order_by("task_assignee")
    )

    task_list = dict()
    prev_worker = ""

    for task in tasks:
        task_color = determine_task_color(
            task.task_status.name, task.task_start_date, task.task_end_date
        )

        if (
                f"{task.task_assignee.first_name} {task.task_assignee.last_name}"
                not in task_list.keys()
        ):
            task_list[
                f"{task.task_assignee.first_name} {task.task_assignee.last_name}"
            ] = dict()

        if (
                "tasks"
                not in task_list[
            f"{task.task_assignee.first_name} {task.task_assignee.last_name}"
        ].keys()
        ):
            task_list[
                f"{task.task_assignee.first_name} {task.task_assignee.last_name}"
            ]["tasks"] = dict()

        if (
                task.id
                not in task_list[
            f"{task.task_assignee.first_name} {task.task_assignee.last_name}"
        ]["tasks"].keys()
        ):
            task_list[
                f"{task.task_assignee.first_name} {task.task_assignee.last_name}"
            ]["tasks"][task.id] = dict()

        task_list[f"{task.task_assignee.first_name} {task.task_assignee.last_name}"][
            "tasks"
        ][task.id].update(
            {
                "id": task.id,
                "title": f"{task.get_activity_name()} {task.task_plan.crop.name} in {task.task_plan.location.name}",
                "start": datetime.strftime(task.task_start_date, "%Y-%m-%d"),
                "end": datetime.strftime(task.task_end_date, "%Y-%m-%d"),
                "description": task.task_notes,
                "className": task_color,
                "location": task.task_plan.location.name,
                "organizer": f"{task.task_creator.first_name} {task.task_creator.last_name}",
            }
        )
    return task_list


def generate_task_weather(request, tasks):
    """
    Based off the list of tasks, retrieve the task location's weather info and associate it with the task.
    :param request:
    :param tasks:
    :return:
    """
    if 'weather' not in request.session.keys():
        generate_location_weather(request)
    task_weather = dict()

    for task in tasks:
        location = str(task.task_plan.location.id)
        task_weather[str(task.id)] = request.session["weather"][location]

    return task_weather


def create_notification(action, task, request, **kwargs):
    """
    Create a notification and determine who gets the notification.
    :param action: what action is being taken on the task
    :param task: The task sqlalchemy object
    :param request: session info object
    :return:
    """
    work_order_assignees = kwargs.get("work_order_assignees", None)

    valid_actions = ["create", "update", "work_order"]
    special_status = ["accepted", "declined", "completed"]
    user_first_name = request.user.first_name
    user_first_name = user_first_name.capitalize()
    user_last_name = request.user.last_name
    user_last_name = user_last_name.capitalize()
    user_name = f"{user_first_name} {user_last_name}"

    if action not in valid_actions:
        messages.add_message(
            request,
            messages.ERROR,
            f"Invalid action type.  Valid actions are: {valid_actions}.",
        )

    try:
        task_assignee = task.task_assignee
    except ShepherdUser.DoesNotExist:
        task_assignee = None

    if task.task_creator == request.user and task_assignee is not None:
        recipient = task.task_assignee.id
    elif task_assignee == request.user:
        recipient = task.task_creator.id
    else:
        recipient = None

    if action == "create":
        if (
                task.task_creator != task_assignee
                and task_assignee is not None
                and recipient is not None
        ):
            # Send assignee or creator notification if they aren't the same person.
            devices = FCMDevice.objects.filter(user_id=recipient, active=True).distinct(
                "device_id", "registration_id"
            )
            title = "New Task Assigned"
            body = f"You have been assigned a {task.get_activity_name().lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} by {user_name}."

            send_notification(devices=devices, title=title, body=body)
        elif task_assignee is None:
            # If no assignee, send to everyone but the creator on the given farm.
            farm_users = get_farm_users(task)
            devices = FCMDevice.objects.filter(
                user_id__in=farm_users, active=True
            ).distinct("device_id", "registration_id")
            title = "New Available Task"
            body = f"A new {task.get_activity_name().lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been made available by {user_name}."

            send_notification(devices=devices, title=title, body=body)

    elif action == "update":
        if task.task_creator != task_assignee and task_assignee is not None:
            # Send assignee/creator notification if they aren't the same person.
            devices = FCMDevice.objects.filter(user_id=recipient, active=True).distinct(
                "device_id", "registration_id"
            )

            if task.task_status.name in special_status:
                notification_status = task.task_status.name
            else:
                notification_status = "updated"

            title = f"A Task Has Been {notification_status.capitalize()}"
            body = f"The {task.get_activity_name().lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been {notification_status} by {user_name}."

            send_notification(devices=devices, title=title, body=body)

            if task.task_status.name == "declined":
                # When task is declined, the farm users need to also be notified.
                farm_users = get_farm_users(task)
                devices = FCMDevice.objects.filter(
                    user_id__in=farm_users, active=True
                ).distinct("device_id", "registration_id")
                title = "Declined Task Available"
                body = f"The {task.get_activity_name().lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} is now available."

        elif task_assignee is None:
            # If no assignee, send to everyone but the creator on the given farm.
            farm_users = get_farm_users(task)
            devices = FCMDevice.objects.filter(
                user_id__in=farm_users, active=True
            ).distinct("device_id", "registration_id")
            title = "An Available Task Has Been Updated"
            body = f"The {task.get_activity_name().lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been updated by {user_name}."

            send_notification(devices=devices, title=title, body=body)
    elif action == "work_order":

        devices = (
            FCMDevice.objects.filter(user_id__in=work_order_assignees, active=True)
                .distinct("device_id", "registration_id")
                .exclude(user_id=task.task_creator)
        )
        title = "New Available Task"
        body = f"A new {task.get_activity_name.lower()} task for {task.task_plan.crop.name.lower()} in {task.task_plan.location.name} has been made available by {user_name}."

        send_notification(devices=devices, title=title, body=body)


def get_farm_users(task):
    """
    For the given task, get the farm's users, except the creator.
    :param task:
    :return:
    """

    return ShepherdUser.objects.filter(
        farm_members__farm__location__plan=task.task_plan_id
    ).exclude(id=task.task_creator_id)


def send_notification(devices, title, body):
    """
    Basic send message
    :param devices: query result object of firebase devices to send notifications to
    :param title: String title of the notification
    :param body: String body of the notification
    :return:
    """
    try:
        devices.send_message(
            title=title, body=body, sound=True, api_key=os.getenv("fcm_server_key")
        )
    except:
        messages.add_message(messages.ERROR, "Notification unable to be sent.")
