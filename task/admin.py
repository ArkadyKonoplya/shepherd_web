from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from task.models import (
    Message,
    Task,
    TaskHistory,
    TaskStatus,
)
from activity.models import Activity, ActivityDetail


class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class ActivityTranslatedAdmin(ActivityAdmin, TranslationAdmin):
    pass


admin.site.register(Activity, ActivityTranslatedAdmin)


class ActivityDetailAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class ActivityDetailTranslatedAdmin(ActivityDetailAdmin, TranslationAdmin):
    pass


admin.site.register(ActivityDetail, ActivityDetailTranslatedAdmin)


class TaskStatusAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class TaskStatusTranslatedAdmin(TaskStatusAdmin, TranslationAdmin):
    pass


admin.site.register(TaskStatus, TaskStatusTranslatedAdmin)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "farm",
        "task",
        "recipient",
        "sender",
        "message_year",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "task_creator",
        "task_assignee",
        "task_activity",
        "task_start_date",
        "task_end_date",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):

    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "id",
        "task_id",
        "update_user",
        "task_status",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
