from uuid import uuid4

from django import forms

from .models import Inventory, ShoppingList
from farm.models import Farm
from field.models import Location


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["item", "quantity", "unit_of_measure", "location"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.farm = Farm.objects.get(member_farms__user=self.user.id, member_farms__default_farm=True)

        super(InventoryForm, self).__init__(*args, **kwargs)

        self.fields["location"].queryset = Location.objects.filter(
            organization=self.farm
        )


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ["item", "quantity", "unit_of_measure", "location"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.farm = Farm.objects.get(member_farms__user=self.user.id, member_farms__default_farm=True)

        super(ShoppingListForm, self).__init__(*args, **kwargs)

        self.fields["location"].queryset = Location.objects.filter(
            organization=self.farm
        )
