from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from activity.models import BaseActivity, Activity, CustomActivity
from activity.forms import CustomActivityForm
from farm.models import Farm


@login_required
def custom_activity_create(request):

    form = CustomActivityForm(request.POST or None)

    if form.is_valid():
        custom_activity = form.save(commit=False)
        custom_activity.farm_id = request.session["farm"]
        custom_activity.created_at = datetime.now()
        custom_activity.created_by = request.user.id
        custom_activity.modified_at = datetime.now()
        custom_activity.modified_by = request.user.id
        custom_activity.save()

        return redirect(farm_custom_activity_list)

    return render(request, "activity/custom_activity_form.html", {"form": form, "title": "Create Custom Activity"})


@login_required
def custom_activity_detail(request, pk):
    # Check if the activity is part of the master activity list. If so, user should only be able to select to
    # enable/disable availability.
    # If a custom activity for the farm, they can edit it.  Any custom activity needs to be compared to the master list
    # and if already there, enable it and send alert.

    activity_instance = CustomActivity.objects.get(pk=pk)

    form = CustomActivityForm(request.POST or None, instance=activity_instance)

    if form.is_valid():
        custom_activity = form.save(commit=False)
        custom_activity.modified_at = datetime.now()
        custom_activity.modified_by = request.user.id
        custom_activity.save()

        return redirect(farm_custom_activity_list)

    return render(request, "activity/custom_activity_form.html", {"form": form, "title": "Update Custom Activity", "pk": pk})


@login_required
def farm_custom_activity_list(request):

    # Need to show all available activities for the farm and designate them as their type (Farm Type, Custom, Crop specifics)

    if "farm" not in request.session:
        farm = Farm.objects.get(
            member_farms__default_farm=True, member_farms__user_id=request.user.id
        )
        request.session["farm"] = str(farm.id)

    activities = get_farm_activity_list(request)

    return render(request, "activity/farm_activities.html", {"activities": activities})


def get_farm_activity_list(request):
    """
    Based off the user's default farm, provide a list of activites that combines the
    filtered list and custom list or the list for the farm's type, or the master list.
    :param request:
    :return:
    """
    activity_list = dict()

    farm_type_activities = Activity.objects.filter(farmtypeactivityrel__farm_type__farm_farm_types__farm__id=request.session["farm"]).distinct()

    if farm_type_activities.count() > 0:

        activity_list['Farm Type'] = farm_type_activities

    else:
        activity_list['Default'] = Activity.objects.all().distinct()

    farm_crop_activities = Activity.objects.filter(crop_activities__crop__plan__planner__farm_members__farm_id=request.session['farm']).distinct()

    if farm_crop_activities.count() > 0:

        activity_list['Crop'] = farm_crop_activities

    farm_custom_activities = CustomActivity.objects.filter(farm_id=request.session['farm']).distinct()

    if farm_custom_activities.count() > 0:

        activity_list['Custom'] = farm_custom_activities

    return activity_list
