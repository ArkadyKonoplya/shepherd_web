from django import forms

from .models import CustomActivity


class CustomActivityForm(forms.ModelForm):
    class Meta:
        model = CustomActivity
        fields = ["name", "requires_crop"]
        labels = {
            "name": "Custom Activity Name",
            "requires_crop": "Crop Required?"
        }