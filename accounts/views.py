from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from cart.models import Cart, CartItem
from products.models import Product
from .forms import SignupForm, SigninForm, UserValidationForm
from .models import User, OTP
from .serializers import UserSerializer
from utils import fetch, send_meassage


class SignupView(View):

    template_name = "accounts/signup.html"
    form = SignupForm

    def sync_session_cart(self, request, cart):
        session = request.session

        if "cart" not in session:
            return False

        my_cart = session["cart"]

        for product in my_cart:
            prod = Product.objects.get(pk=product["product"])
            quantity = product["quantity"]
            CartItem.objects.create(cart=cart, product=prod, quantity=quantity)

        # pop is safer than del
        request.session.pop("cart", None)

        return True


    def render(self, request, form):
        url = fetch(["accounts/6310507.jpg"])
        return render(request, self.template_name, {"form": form, "url": url[0]})

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

                cart, created = Cart.objects.get_or_create(user=user)
                self.sync_session_cart(request, cart)

                messages.success(request, "You are successfully registered")

                login(request, user)
                return redirect("pages:home")

            except Exception as e:

                form.add_error("password2", str(e))
        self.render(request, form)
    
    # custom mixin
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            messages.warning(request, "You must be logged out to access this page.")
            return redirect('pages:home')
        
        return super().dispatch(request, *args, **kwargs)


class SigninView(View):

    template_name = "accounts/signin.html"
    form = SigninForm

    def render(self, request, form):
        url = fetch(["accounts/3094352.jpg"])
        return render(request, self.template_name, {"form": form, "url": url[0]})

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

                login(request, user)
                messages.success(request, "You are logedin successfully")
                return redirect("pages:home")

            else:
                form.add_error("password", "Email and Password are do not match!")
                return self.render(request, form)

        return self.render(request, form)
    
    # custom mixin
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            messages.error(request, "You must be logged out to access this page.")
            return redirect('pages:home')
        
        return super().dispatch(request, *args, **kwargs)


class ValidationView(LoginRequiredMixin, View):

    login_url = "/accounts/signin/"
    class_form = UserValidationForm
    template_name = "accounts/validation.html"

    def get(self, request):

        form = self.class_form()
        return render(request, self.template_name, {"form": form})

    def post(self, request):

        form = self.class_form(request.post)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            user = User.objects.filter(phone_number=phone_number).first()

            if user:
                otp = OTP.objects.filter(user=user, used=False).first()

                if otp and otp.is_valid():
                    user.validate = True
                    user.save()
                    messages.success(request, "Your account is successfully validated!")
                    otp.mark_used()

                    return redirect("pages:home")
                else:
                    messages.error("Invalid or expired OTP!")
                    return render(request, self.template_name, {"form": form})

        messages.error(request, "This Phone Number does not exist")
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):

    login_url = "/accounts/signin/"

    def get(self, request):

        logout(request)
        messages.success(request, "You are logedout successfully")
        return redirect("pages:home")


class UserAPI(APIView):

    def get(self, request):

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateOTP(LoginRequiredMixin, APIView):

    def get(self, request):
        try:
            user = User.objects.get(email=request.user.email)

        except User.DoesNotExist:
            return Response({"error": "You must login before validate"}, status=status.HTTP_400_BAD_REQUEST)

        otp = OTP.create_otp(user)
        # Send SMS to user Phone Number
        send_meassage(otp.code, request.GET.get("phone_number"))

        return Response({'otp': otp.code, 'expires_at': otp.expires_at}, status=status.HTTP_200_OK)
