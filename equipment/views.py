from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect

from .models import Equipment, EquipmentModel, EquipmentMake
from .forms import EquipmentForm

from task.models import TaskHistory


class ProfileView(generic.UpdateView):
    model = Equipment
    form_class = EquipmentForm
    success_url = reverse_lazy("equipment_profile")
    template_name = "equipment/profile.html"

    def get(self, request, *args, **kwargs):
        equipment = kwargs.get('pk', None)
        equipment = get_object_or_404(Equipment, id=equipment)
        form = self.form_class(user=request.user.id)

        tasks = TaskHistory.objects.select_related("task_status", "task_id", "task_id__task_plan__crop", "task_id__task_activity", "task_id__task_plan__location", "update_user").filter(task_id__equipment_task__equipment__id=equipment.id).order_by("-status_date_change")[:5]

        return render(request, self.template_name, {"form": form, "equipment": equipment, "tasks": tasks,})


@login_required
def equipment_create(request):

    form = EquipmentForm(request.POST or None, user=request.user.id)

    if form.is_valid():
        form.save()

    return render(request, "equipment/create_equipment.html", {"form": form})


@login_required
def equipment_detail(request, pk):
    equipment_instance = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(
        request.POST or None, instance=equipment_instance, user=request.user
    )

    if form.is_valid():
        form.save()
        return redirect("equipment_detail", pk=equipment_instance.id)

    return render(
        request,
        "equipment/update_equipment.html",
        {"form": form, "uuid": equipment_instance.id},
    )


@login_required
def equipment_list(request):

    equipment = Equipment.objects.select_related(
        "make_model__equipment_type", "make_model", "make_model__make"
    ).filter(farm__member_farms__user_id=request.user.id)

    return render(request, "equipment/equipment.html", {"equipment_list": equipment})
