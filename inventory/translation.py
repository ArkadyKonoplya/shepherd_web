from modeltranslation.translator import register, TranslationOptions
from .models import InventoryUnitOfMeasure


@register(InventoryUnitOfMeasure)
class InventoryUnitOfMeasureTranslationOptions(TranslationOptions):
    fields = ('name',)