from modeltranslation.translator import register, TranslationOptions
from .models import TaskStatus
from activity.models import Activity, ActivityDetail


@register(Activity)
class ActivityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ActivityDetail)
class ActivityDetailTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(TaskStatus)
class TaskStatusTranslationOptions(TranslationOptions):
    fields = ('name',)
