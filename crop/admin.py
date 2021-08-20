from django.contrib import admin
from crop.models import Crop
from modeltranslation.admin import TranslationAdmin


class CropAdmin(admin.ModelAdmin):

    readonly_fields = ["id", "created_at", "modified_at", "created_by", "modified_by"]

    list_display = ["name", "created_at", "modified_at", "created_by", "modified_by"]


class CropTranslatedAdmin(CropAdmin, TranslationAdmin):
    pass


admin.site.register(Crop, CropTranslatedAdmin)