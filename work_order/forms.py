from datetime import datetime

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from equipment.models import Equipment
from farm.models import Farm
from plan.models import Plan
from user.models import ShepherdUser
from work_order.models import WorkOrder


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            "work_order_name",
            "activity",
            "start_date",
            "end_date",
            "available_date",
        ]
        labels = {
            "work_order_name": _("Work Order Name"),
            "activity": _("Activity"),
            "available_date": _("Available Date"),
            "start_date": _("Start Date"),
            "end_date": _("End Date"),
        }

    def __init__(self, *args, **kwargs):

        super(WorkOrderForm, self).__init__(*args, **kwargs)

        self.fields["available_date"].widget.attrs.update(
            {
                "class": "form-control datetimepicker",
                "placeholder": "yyyy/mm/dd",
                "data-options": '{"static":"true","enableTime":"false","dateFormat":"Y-m-d"}',
            }
        )
        self.fields["start_date"].widget.attrs.update(
            {
                "class": "form-control datetimepicker",
                "placeholder": "yyyy/mm/dd",
                "data-options": '{"static":"true","enableTime":"false","dateFormat":"Y-m-d"}',
            }
        )
        self.fields["end_date"].widget.attrs.update(
            {
                "class": "form-control datetimepicker",
                "placeholder": "yyyy/mm/dd",
                "data-options": '{"static":"true","enableTime":"false","dateFormat":"Y-m-d"}',
            }
        )


class WorkOrderTaskForm(forms.Form):
    send_all_workers = forms.BooleanField(
        label="Send task to all selected workers?", required=False
    )

    def __init__(self, *args, **kwargs):
        today = datetime.now()

        self.user = kwargs.pop("user")
        self.farm = Farm.objects.get(
            member_farms__user=self.user.id, member_farms__default_farm=True
        )
        super(WorkOrderTaskForm, self).__init__(*args, **kwargs)

        task_plans = (
            Plan.objects.select_related("location", "crop")
            .filter(planner__farm_members__farm=self.farm.id, plan_year__gte=today.year)
            .order_by("plan_year", "location__name", "crop__name")
        )
        task_assignees = ShepherdUser.objects.filter(farm_members__farm=self.farm.id)
        equipment_set = Equipment.objects.filter(farm=self.farm.id, deleted_at=None)

        self.fields["equipment"] = forms.ModelMultipleChoiceField(
            label="Equipment", queryset=equipment_set
        )
        self.fields["equipment"].widget.attrs.update({"class": "form-control"})

        self.fields["task_plan"] = forms.ModelMultipleChoiceField(
            label="Plan Year/Field/Crop", queryset=task_plans
        )
        self.fields["task_plan"].widget.attrs.update({"class": "form-control"})

        self.fields["task_assignee"] = forms.ModelMultipleChoiceField(
            label="Task Assignee", queryset=task_assignees
        )
        self.fields["task_assignee"].widget.attrs.update({"class": "form-control"})
        self.fields["task_assignee"].required = False
