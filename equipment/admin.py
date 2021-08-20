from django.contrib import admin
from equipment.models import Equipment, EquipmentMake, EquipmentModel, EquipmentType
from modeltranslation.admin import TranslationAdmin


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):

    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "id",
        "make_model",
        "name",
        "farm",
        "serial_num",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(EquipmentMake)
class EquipmentMakeAdmin(admin.ModelAdmin):

    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "make",
        "name",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


class EquipmentTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class EquipmentTypeTranslatedAdmin(EquipmentTypeAdmin, TranslationAdmin):
    pass


admin.site.register(EquipmentType, EquipmentTypeTranslatedAdmin)
