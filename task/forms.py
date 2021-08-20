from datetime import datetime

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from activity.views import get_farm_activity_list

from .models import Task
from equipment.models import Equipment
from farm.models import Farm
from plan.models import Plan
from user.models import ShepherdUser


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "task_plan",
            "task_activity",
            "task_assignee",
            "equipment",
            "task_available_date",
            "task_start_date",
            "task_end_date",
            "is_draft",
            "task_notes",
        ]
        labels = {
            "task_plan": _("Plan Year/Field/Crop"),
            "task_activity": _("Category"),
            "task_assignee": _("Worker"),
            "equipment": _("Machinery"),
            "task_available_date": _("Task Available Date"),
            "task_start_date": _("Start Date"),
            "task_end_date": _("End Date"),
            "is_draft": _("Is Draft"),
            "task_notes": _("Task Notes"),
        }

    def __init__(self, *args, **kwargs):

        current_year = datetime.now()
        current_year = current_year.date()
        current_year = current_year.strftime("%Y")

        self.request = kwargs.pop("request")
        self.user = self.request.user
        self.farm = Farm.objects.get(
            member_farms__user=self.user.id, member_farms__default_farm=True
        )
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["task_available_date"].widget.attrs.update(
            {
                "class": "form-control datetimepicker",
                "placeholder": "yyyy/mm/dd",
                "data-options": '{"static":"true","enableTime":"false","dateFormat":"Y-m-d"}',
            }
        )
        self.fields["task_start_date"].widget.attrs.update(
            {
                "class": "form-control datetimepicker",
                "placeholder": "yyyy/mm/dd",
                "data-options": '{"static":"true","enableTime":"false","dateFormat":"Y-m-d"}',
            }
        )
        self.fields["task_end_date"].widget.attrs.update(
            {
                "class": "form-control datetimepicker",
                "placeholder": "yyyy/mm/dd hh:mm",
                "data-options": '{"static":"true","enableTime":"false","dateFormat":"Y-m-d"}',
            }
        )

        self.fields["equipment"].queryset = Equipment.objects.filter(farm=self.farm.id)
        self.fields["equipment"].widget.attrs.update({"class": "form-control"})
        self.fields["task_plan"].queryset = (
            Plan.objects.select_related("location", "crop")
            .filter(
                planner__farm_members__farm=self.farm.id,
            )
            .order_by("location__name", "crop__name")
        )
        self.fields["task_plan"].widget.attrs.update({"class": "form-control"})
        self.fields["task_plan"].queryset = Plan.objects.filter(plan_year__gte=current_year, planner__farm_members__farm=self.farm.id,)
        self.fields["task_activity"].choices = make_activity_list(self.request)
        self.fields["task_activity"].widget.attrs.update({"class": "form-control"})
        self.fields["task_assignee"].queryset = ShepherdUser.objects.filter(
            farm_members__farm=self.farm.id
        )
        self.fields["task_assignee"].widget.attrs.update({"class": "form-control"})
        self.fields["task_notes"].widget.attrs.update({"class": "form-control"})
        self.fields["is_draft"].widget.attrs.update(
            {"class": "form-control form-check-input"}
        )


def make_activity_list(request):
    """
    Need to convert the dictionary list from get_farm_activity_list to something the form can use.
    :return:
    """

    activities = get_farm_activity_list(request)
    activity_dropdown_choices = list()

    if 'Farm Type' in activities.keys():

        activity_list = activities['Farm Type']

    else:
        activity_list = activities['Default']

    for activity in activity_list:
        activity_dropdown_choices.append((activity.id, activity.name))

    if 'Crop' in activities.keys():
        activity_list = activities['Crop']

    for activity in activity_list:
        activity_dropdown_choices.append((activity.id, activity.name))

    if 'Custom' in activities.keys():
        activity_list = activities['Custom']

        for activity in activity_list:
            activity_dropdown_choices.append((activity.id, activity.name))

    return list(dict.fromkeys(activity_dropdown_choices))






