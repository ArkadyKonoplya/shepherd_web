from django.contrib import admin

from .models import (
    ShepherdUser,
    UserCertifications,
    UserPointActivity,
    PointActivityType,
    PointLevels,
)


@admin.register(ShepherdUser)
class ShepherdUserAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "username",
        "first_name",
        "last_name",
        "date_joined",
        "current_points",
        "lifetime_points",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(UserCertifications)
class UserCertificationsAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "cert_user",
        "cert_name",
        "cert_body",
        "cert_date",
        "cert_expire_date",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(UserPointActivity)
class UserPointActivityAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "user",
        "point_activity",
        "points_earned_spent",
        "activity_date",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(PointLevels)
class PointLevelsAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "point_level_name",
        "points_required",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(PointActivityType)
class PointActivityTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "point_activity_name",
        "default_point_value",
        "max_times_earnable",
        "available_from_date",
        "available_to_date",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
