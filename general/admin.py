from django.contrib import admin

from general.models import Acknowledgements


@admin.register(Acknowledgements)
class AcknowledgementsAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "acknowledgement",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
