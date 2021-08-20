from django.contrib import admin
from image.models import BackgroundImage


@admin.register(BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "filename",
        "description",
        "image_for_day",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
