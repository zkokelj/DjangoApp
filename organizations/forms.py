from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Organization


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class EditOrganization(forms.ModelForm):
    name = forms.TextInput()
    address = forms.TextInput()
    tax_number = forms.TextInput()
    mobile_number = forms.TextInput()

    class Meta:
        model = Organization
        fields = ["name", "address", "tax_number", "mobile_number"]
