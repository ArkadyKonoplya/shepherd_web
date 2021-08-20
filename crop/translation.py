from modeltranslation.translator import register, TranslationOptions
from .models import Crop


@register(Crop)
class CropTranslationOptions(TranslationOptions):
    fields = ('name',)
