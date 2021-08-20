from modeltranslation.translator import register, TranslationOptions
from .models import LocationType


@register(LocationType)
class LocationTypeTranslationOptions(TranslationOptions):
    fields = ('name',)