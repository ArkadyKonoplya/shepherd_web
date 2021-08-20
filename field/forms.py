from django import forms
from django.contrib.gis import admin

from leaflet.forms.widgets import LeafletWidget

from .models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "legal_name", "type", "acres", "drawn_area"]
        labels = {
            "name": "Location Name",
            "legal_name": "Legal Name",
            "type": "Location Type",
            "drawn_area": "Drawn Area",
        }
        widgets = {"drawn_area": LeafletWidget()}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")

        super(LocationForm, self).__init__(*args, **kwargs)
