from django import forms


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
