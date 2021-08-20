from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Equipment
from farm.models import Farm


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["name", "farm", "make_model", "serial_num"]
        labels = {
            "name": _("Equipment Name"),
            "farm": _("Farm"),
            "make_model": _("Make and Model"),
            "serial_num": _("Serial Number"),
        }

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user")

        super(EquipmentForm, self).__init__(*args, **kwargs)

        self.fields["farm"].queryset = Farm.objects.filter(
            member_farms__user_id=self.user
        )
