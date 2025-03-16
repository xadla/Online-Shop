from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


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


class SignupForm(forms.Form):

    first_name = forms.CharField(
        label="First Name",
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your first name"},
        ),
        help_text="You should enter your first name in this field",
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your last name"},
        ),
        help_text="You should enter your last name in this field",
    )

    email = forms.EmailField(
        label="Email",
        max_length=200,
        required=False,
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email"},
        ),
        help_text="You should enter your Email in this field",
    )

    password1 = forms.CharField(
        label="Password",
        max_length=200,
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"}
        ),
        help_text="You should enter your password in this field",
    )

    password2 = forms.CharField(
        label="Confirm Password",
        max_length=200,
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password"}
        ),
        help_text="You should enter your password again in this field",
    )


class SigninForm(forms.Form):

    email = forms.EmailField(
        label="Email",
        max_length=200,
        required=False,
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email"},
        ),
        help_text="You should enter your Email in this field",
    )

    password = forms.CharField(
        label="Password",
        max_length=200,
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"}
        ),
        help_text="You should enter your password in this field",
    )
