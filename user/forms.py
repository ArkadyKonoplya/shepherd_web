from django import forms
from user.models import ShepherdUser
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = ShepherdUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "timezone",
            "password1",
            "password2",
        ]

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ShepherdUser
        fields = ["first_name", "last_name", "email", "phone_number", "timezone"]
