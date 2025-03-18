from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from cart.models import Cart
from .forms import SignupForm, SigninForm
from .models import User


class SignupView(View):

    template_name = "accounts/signup.html"
    form = SignupForm

    def render(self, request, form):
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form()
        return self.render(request, form)

    def post(self, request):

        form = self.form(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            if User.objects.filter(email=email).exists():

                form.add_error("email", "This email is used before!")
                return self.render(request, form)

            try:

                pass1 = form.cleaned_data["password1"]
                pass2 = form.cleaned_data["password2"]

                if pass1 != pass2:
                    form.add_error("password2", "Passwords do not match!")
                    return self.render(request, form)

                user = User.objects.create_user(
                    email=email,
                    password=pass1,
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"]
                )

                login(request, user)
                return redirect("pages:home")

            except Exception as e:

                form.add_error("password2", str(e))
        self.render(request, form)


class SigninView(View):

    template_name = "accounts/signin.html"
    form = SigninForm

    def render(self, request, form):
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form()
        return self.render(request, form)

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(email=email, password=password)

            if user is not None:
                # create a cart for user
                cart, created = Cart.objects.get_or_create(user=user)
                # login a user
                login(request, user)
                return redirect("pages:home")

            else:
                form.add_error("password", "Email and Password are not match!")
                return self.render(request, form)

        return self.render(request, form)


class LogoutView(View):

    def get(self, request):

        logout(request)
        return redirect("pages:home")
