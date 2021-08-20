import pytz

from django.utils import timezone
from django.db.models import signals
from functools import partial


class AuditTrackMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in ("GET", "HEAD", "OPTIONS", "TRACE"):
            if hasattr(request, "user") and request.user.is_authenticated:
                user = request.user
            else:
                user = None

            mark_whodid = partial(self.mark_whodid, user)
            signals.pre_save.connect(
                mark_whodid,
                dispatch_uid=(
                    self.__class__,
                    request,
                ),
                weak=False,
            )
        response = self.get_response(request)
        signals.pre_save.disconnect(
            dispatch_uid=(
                self.__class__,
                request,
            )
        )

        return response

    def mark_whodid(self, user, sender, instance, **kwargs):
        if user is not None:
            if not getattr(instance, "created_by", None):
                instance.created_by = user.id

            if hasattr(instance, "modified_by"):
                instance.modified_by = user.id

        else:
            if not getattr(instance, "created_by", None):
                instance.created_by = None

            if hasattr(instance, "modified_by"):
                instance.modified_by = None
