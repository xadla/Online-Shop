from django.urls import path


from .views import (
    SignupView,
    SigninView,
    LogoutView,
    ValidationView,
    UserAPI,
    GenerateOTP,
)


app_name = "accounts"
urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("validate/", ValidationView.as_view(), name="validate"),
    path("users/", UserAPI.as_view(), name="user-api"),
    path("generate/", GenerateOTP.as_view(), name="generate"),
]
