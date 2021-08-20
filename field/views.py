import datetime
import os

from darksky.api import DarkSky

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import LocationForm
from .models import Location

from task.models import TaskHistory

darksky_key = os.getenv("darksky_api_key")


class ProfileView(generic.UpdateView):
    model = Location
    form_class = LocationForm
    success_url = reverse_lazy("location_profile")
    template_name = "field/profile.html"

    def get(self, request, *args, **kwargs):
        location = kwargs.get('pk', None)
        location = get_object_or_404(Location, id=location)
        form = self.form_class(user=request.user)

        tasks = TaskHistory.objects.select_related("task_status", "task_id", "task_id__task_plan__crop", "task_id__task_plan__location", "update_user").filter(task_id__task_plan__location__id=location.id).order_by("-status_date_change")[:5]

        return render(request, self.template_name, {"form": form, "location": location, "tasks": tasks, "weather": request.session["weather"][str(location.id)]})


@login_required
def location_create(request):

    form = LocationForm(request.POST or None, user=request.user)

    if form.is_valid():
        location = form.save(commit=False)
        location.created_by = request.user
        location.modified_by = request.user
        location.save()

        messages.add_message(
            request, messages.SUCCESS, "Location was created successfully!"
        )

    else:
        messages.add_message(request, messages.ERROR, form.errors)

    return render(
        request,
        "field/create_location.html",
    )


@login_required
def location_detail(request, pk):
    location_instance = get_object_or_404(Location, pk=pk)
    form = LocationForm(
        request.POST or None, instance=location_instance, user=request.user
    )

    return render(
        request,
        "field/update_location.html",
        {"form": form, "uuid": location_instance.id, "location_weather": request.session['weather']},
    )


@login_required
def location_list(request):

    locations = generate_location_list(request.user.id)
    if 'weather' not in request.session.keys():
        generate_location_weather(request)

    return render(
        request,
        "field/locations.html",
        {
            "locations": locations,
            "location_weather": request.session['weather'],
        },
    )


def generate_location_weather(request):
    """
    Based on the logged in user, generate the Farm's locations' weather info and store it in cache.
    :param request:
    :return:
    """
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)

    locations = generate_location_list(request.user.id)
    request.session['weather'] = dict()

    darksky = DarkSky(darksky_key)
    for location in locations:

        geocenter = location.geo_center
        forecast = darksky.get_forecast(
            latitude=geocenter[1], longitude=geocenter[0]
        )

        day_data = forecast.daily.data[0]

        request.session['weather'][str(location.id)] = dict()
        request.session['weather'][str(location.id)]['summary'] = forecast.currently.summary
        request.session['weather'][str(location.id)]['wind_speed'] = forecast.currently.wind_speed
        request.session['weather'][str(location.id)]['temp'] = forecast.currently.temperature
        request.session['weather'][str(location.id)]['low_temp'] = day_data.temperature_low
        request.session['weather'][str(location.id)]['high_temp'] = day_data.temperature_high

        historical_weather = darksky.get_time_machine_forecast(
            latitude=geocenter[1], longitude=geocenter[0], time=yesterday
        )

        for day in historical_weather.daily.data:
            request.session['weather'][str(location.id)]['yesterday_precip'] = round(
                day.precip_intensity * day.precip_probability, 2
            )


def generate_location_list(user_id):
    """
    Based on the user id, get the list of locations for the given farm for the locations page.
    :param user_id:
    :return:
    """
    locations = Location.objects.select_related("type").filter(
        organization__member_farms__user_id=user_id
    )

    return locations
