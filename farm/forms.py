from django import forms

from .models import Farm
from field.models import Location


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = [
            "name",
            "type",
            "main_location",
        ]

        labels = {
            "name": "Farm Name",
            "type": "Farm Type",
            "main_location": "Farm Main Location",
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.locations = Location.objects.filter(organization__id=self.request.session["farm"])

        super(FarmForm, self).__init__(*args, **kwargs)
        self.fields["main_location"].queryset = self.locations
        self.fields["main_location"].widget.attrs.update({"class": "form-control"})