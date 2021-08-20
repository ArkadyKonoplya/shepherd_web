from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from task.views import create_notification

from task.models import Task, TaskStatus
from work_order.models import WorkOrder, WorkOrderTaskRel, WorkOrderEquipmentRel
from work_order.forms import WorkOrderForm, WorkOrderTaskForm


@login_required
def work_order_create(request):

    form = WorkOrderForm(request.POST or None, prefix="work_order")

    if form.is_valid():
        work_order = form.save(commit=False)
        work_order.created_at = datetime.now()
        work_order.modified_at = datetime.now()
        work_order.created_by = request.user.id
        work_order.modified_by = request.user.id
        work_order.save()

        return redirect("work_order_detail", pk=work_order.id)

    return render(request, "work_orders/create_work_order.html", {"form": form})


@login_required
def work_order_detail(request, pk):

    work_order_instance = get_object_or_404(WorkOrder, pk=pk)

    if "work_order_form" in request.POST:

        form = WorkOrderForm(
            request.POST or None, instance=work_order_instance, prefix="work_order"
        )
    else:
        form = WorkOrderForm(instance=work_order_instance, prefix="work_order")

    task_form = WorkOrderTaskForm(
        request.POST or None, user=request.user, prefix="task"
    )

    tasks = Task.objects.filter(work_order_tasks__work_order_id=work_order_instance.id)

    if form.is_valid():
        work_order = form.save(commit=False)
        if work_order.work_order_name is None:
            work_order.work_order_name = f"{work_order.activity.name} - {task_form.task_plan.crop.name} - {task_form.task_plan.plan_year}"  # TODO Fix this as this won't work... task_form is NOT set at the same time...
        work_order.farm = ""
        work_order.modified_by = request.user.id
        work_order.modified_at = datetime.now()
        work_order.save()

    if task_form.is_valid():
        data = task_form.cleaned_data

        if data["send_all_workers"] is True:
            # Send_all_workers triggers how tasks are created and users notified.  Selected workers get notifications.

            if not data["task_assignee"]:

                messages.add_message(
                    request, messages.ERROR, "No workers have been selected."
                )

            else:
                for plan in data["task_plan"]:
                    for assignee in data["task_assignee"]:
                        # If workers are selected, and send_all_workers is True, send individual tasks to each worker
                        # for each plan
                        new_task = Task(
                            task_creator=request.user,
                            task_status=TaskStatus.objects.get(name="assigned"),
                            task_assignee=assignee,
                            task_plan=plan,
                            task_start_date=work_order_instance.start_date,
                            task_end_date=work_order_instance.end_date,
                            task_available_date=work_order_instance.available_date,
                            task_activity_id=work_order_instance.activity.id,
                        )
                        new_task.save()

                        work_order_instance.total_tasks = (
                            work_order_instance.total_tasks + 1
                        )
                        work_order_instance.save()

                        wo_task = WorkOrderTaskRel(
                            work_order=work_order_instance,
                            task=new_task,
                            created_by=request.user.id,
                            modified_by=request.user.id,
                        )
                        wo_task.save()

                        create_notification(
                            action="create", task=new_task, request=request
                        )

        else:

            for plan in data["task_plan"]:
                new_task = Task(
                    task_creator=request.user,
                    task_status=TaskStatus.objects.get(name="available"),
                    task_plan=plan,
                    task_start_date=work_order_instance.start_date,
                    task_end_date=work_order_instance.end_date,
                    task_available_date=work_order_instance.available_date,
                    task_activity_id=work_order_instance.activity.id,
                )
                new_task.save()

                wo_task = WorkOrderTaskRel(
                    work_order=work_order_instance,
                    task=new_task,
                    created_by=request.user.id,
                    modified_by=request.user.id,
                )
                wo_task.save()

                if not data["task_assignee"]:
                    create_notification(action="create", task=new_task, request=request)
                else:
                    create_notification(
                        action="work_order",
                        task=new_task,
                        request=request,
                        work_order_assignees=data["task_assignee"],
                    )

        for equipment in data["equipment"]:
            new_equipment_rel = WorkOrderEquipmentRel(
                work_order=work_order_instance, equipment=equipment
            )
            new_equipment_rel.save()

    return render(
        request,
        "work_orders/update_work_order.html",
        {
            "form": form,
            "task_form": task_form,
            "uuid": work_order_instance.id,
            "tasks": tasks,
        },
    )


@login_required
def work_order_list(request):
    today = datetime.now()
    table_title = "Work Orders"
    work_orders = WorkOrder.objects.filter()

    work_order_counts = WorkOrder.objects.select_related("work_order_status").values("work_order_status__name").filter(farm=request.session['farm']).annotate(count=Count("work_order_status")).filter(start_date__year__gte=today.year)

    open_work_orders = 0
    in_progress_work_orders = 0
    completed_work_orders = 0

    for count in work_order_counts:
        if count["work_order_status__name"] == "open":
            open_work_orders += count["count"]

        if count["work_order_status__name"] == "in progress":
            in_progress_work_orders += count["count"]

        if count["work_order_status__name"] == "completed":
            completed_work_orders += count["count"]

    return render(
        request,
        "work_orders/work_orders.html",
        {"work_orders": work_orders, "table_title": table_title, "completed_work_orders": completed_work_orders, "in_process_work_orders": in_progress_work_orders, "open_work_orders": open_work_orders},
    )


@login_required
def in_progress_work_orders(request):
    table_title = "In Progress Work Orders"
    today = datetime.today()

    work_orders = WorkOrder.objects.filter(farm__id=request.session["farm"]).filter(
        end_date__gte=today
    )

    return render(
        request,
        "work_orders/work_orders.html",
        {"work_orders": work_orders, "table_title": table_title},
    )


@login_required
def overdue_work_orders(request):
    table_title = "Overdue Work Orders"
    today = datetime.today()

    work_orders = WorkOrder.objects.filter(farm__id=request.session["farm"]).filter(
        end_date__lt=today
    )

    return render(
        request,
        "work_orders/work_orders.html",
        {"work_orders": work_orders, "table_title": table_title},
    )
