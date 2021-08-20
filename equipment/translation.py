from modeltranslation.translator import register, TranslationOptions
from .models import EquipmentType


@register(EquipmentType)
class EquipmentTypeTranslationOptions(TranslationOptions):
    fields = ('name',)