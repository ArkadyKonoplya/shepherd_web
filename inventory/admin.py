from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from inventory.models import Inventory, InventoryUnitOfMeasure, ShoppingList


class InventoryUnitOfMeasureAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class InventoryUnitOfMeasureTranslationAdmin(InventoryUnitOfMeasureAdmin, TranslationAdmin):
    pass


admin.site.register(InventoryUnitOfMeasure, InventoryUnitOfMeasureTranslationAdmin)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "farm_id",
        "location",
        "item",
        "quantity",
        "unit_of_measure",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = [
        "farm_id",
        "location",
        "item",
        "quantity",
        "unit_of_measure",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    ]
