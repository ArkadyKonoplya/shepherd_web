from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from activity.models import FarmTypeActivityRel, CropTypeActivityType


@admin.register(FarmTypeActivityRel)
class FarmTypeActivityRelAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "farm_type",
        "activity_type",
        "sort_order",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(CropTypeActivityType)
class CropTypeActivityTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "crop",
        "activity",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by"
    ]