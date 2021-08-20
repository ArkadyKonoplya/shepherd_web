from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin
from modeltranslation.admin import TranslationAdmin

from field.models import Location, LocationType
from activity.models import LocationTypeActivityType


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    readonly_fields = [
        "id",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "deleted_at",
        "deleted_by",
    ]

    list_display = [
        "name",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "deleted_at",
        "deleted_by",
    ]


class LocationTypeAdmin(admin.ModelAdmin):
    readonly_fields = [
        "id",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "deleted_at",
        "deleted_by",
    ]

    list_display = [
        "name",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "deleted_at",
        "deleted_by",
    ]


class LocationTypeTranslationAdmin(LocationTypeAdmin, TranslationAdmin):
    pass

admin.site.register(LocationType, LocationTypeTranslationAdmin)

@admin.register(LocationTypeActivityType)
class LocationTypeActivityTypeAdmin(admin.ModelAdmin):
    readonly_fields = [
        "id",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "deleted_at",
        "deleted_by",
    ]

    list_display = [
        "location_type",
        "activity_type",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "deleted_at",
        "deleted_by",
    ]
