from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from farm.models import (
    Farm,
    FarmType,
    FarmUsers,
    OrganizationRole,
    OrganizationType,
    OrganizationTypeLocationTypeRel,
    OrganizationRel,
)


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "name",
        "type",
        "code",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(FarmType)
class FarmTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "farm",
        "farm_type",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


# @admin.register(FarmUsers)
# class FarmUsersAdmin(admin.ModelAdmin):
#     readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]
#
#     list_display = ["user", "farm", "role", "created_at", "modified_at", "created_by", "modified_by"]


@admin.register(OrganizationRole)
class OrganizationRoleAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class OrganizationTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class OrganizationTypeTranslationAdmin(TranslationAdmin):
    pass


admin.site.register(OrganizationType, OrganizationTypeTranslationAdmin)


@admin.register(OrganizationTypeLocationTypeRel)
class OrganizationTypeLocationTypeRelAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "farm_type",
        "location_type",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(OrganizationRel)
class OrganizationRel(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "parent_org",
        "child_org",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
