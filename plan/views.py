import json
from datetime import datetime
import os
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from .forms import PlanForm
from .models import Plan


@login_required
def plan_list(request):
    plans = Plan.objects.select_related("location", "crop").filter(planner__farm_members__farm=request.session["farm"]).order_by("-plan_year", "location__name", "crop__name")

    return render(request, "plan/plans.html", {"plans": plans, "table_title": "Farm Plans"})


@login_required
def plan_create(request):

    form = PlanForm(request.POST or None, farm=request.session['farm'])

    if form.is_valid():
        plan = form.save(commit=False)
        plan.planner = request.user
        plan.created_at = datetime.now()
        plan.created_by = request.user.id

        plan.save()

        messages.add_message(request, messages.SUCCESS, "Plan was created successfully!")

    return render(request, "plan/create_plan.html", {"form": form})


@login_required
def plan_detail(request, pk):
    plan_instance = get_object_or_404(Plan, pk=pk)
    form = PlanForm(request.POST or None, instance=plan_instance, farm=request.session['farm'])

    if form.is_valid():
        plan = form.save(commit=False)
        plan.modified_by = request.user.id
        plan.modified_at = datetime.now()
        plan.save()

        messages.add_message(request, messages.SUCCESS, "Plan updated successfully!")

        return redirect("plan_detail", pk=plan_instance.id)

    return render(request, "plan/plan_detail.html", {"form": form, "uuid": plan_instance.id})

