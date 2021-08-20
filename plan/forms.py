from uuid import uuid4

from django import forms

from field.models import Location
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = [
            "plan_year",
            "crop",
            "location"
        ]

        labels = {
            "plan_year": "Plan Year",
        }

    def __init__(self, *args, **kwargs):
        self.farm = kwargs.pop("farm")

        super(PlanForm, self).__init__(*args, **kwargs)

        self.fields["plan_year"].widget.attrs.update(
            {
                'class': 'form-control datetimepicker',
                'placeholder': "yyyy",
                'data-options': '{"static":"true", "enableTime":"false", "dateFormat":"Y"}',
            }
        )

        self.fields['location'].queryset = Location.objects.filter(organization__id=self.farm)