from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls", namespace="pages")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("products/", include("products.urls", namespace="products")),
    path("cart/", include("cart.urls", namespace="cart")),
]
