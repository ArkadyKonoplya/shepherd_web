from modeltranslation.translator import register, TranslationOptions
from .models import OrganizationType


@register(OrganizationType)
class OrganizationTypeTranslationOptions(TranslationOptions):
    fields = ('name',)