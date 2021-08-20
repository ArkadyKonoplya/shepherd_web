from django.contrib import admin

from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):

    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "planner",
        "plan_year",
        "crop",
        "location",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]