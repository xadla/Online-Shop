from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


import re


from .models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "is_admin", "is_active", "phone_number", "address"]


class SignupForm(forms.ModelForm):

    password2 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password..."}
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "password2")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Please Enter your Firstname..."}),
            "last_name": forms.TextInput(attrs={"placeholder": "Please Enter your Lastname..."}),
            "email": forms.EmailInput(attrs={"placeholder": "Please Enter your Email..."}),
            "password": forms.PasswordInput(attrs={"placeholder": "Please Enter your Password..."}),
        }


class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "Please Enter your Email..."}),
            "password": forms.PasswordInput(attrs={"placeholder": "Please Enter your Password..."}),
        }


class UserValidationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["phone_number"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"placeholder": "Please Enter your Phone Number ..."}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if not re.fullmatch(r"^\d{10,15}$", phone_number):
            raise ValidationError("Phone number must be 10-15 digits long and contain only numbers.")

        if not phone_number.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
            raise ValidationError("Invalid phone number format.")

        return phone_number
