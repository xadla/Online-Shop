from django.urls import path


from .views import CategoryView, ProductView, ProductAPI


app_name = "products"
urlpatterns = [
    path("all/", ProductAPI.as_view(), name="products-api"),
    path("<int:id>/", ProductView.as_view(), name="product"),
    path("<str:category>/", CategoryView.as_view(), name="category"),
]
