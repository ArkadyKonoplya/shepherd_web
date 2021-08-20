from django.contrib import admin

from work_order.models import WorkOrder, WorkOrderTaskRel, WorkOrderEquipmentRel


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "id",
        "farm",
        "work_order_name",
        "activity",
        "start_date",
        "end_date",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
