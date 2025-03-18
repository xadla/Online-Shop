from django.urls import path


from .views import CategoryView


app_name = "products"
urlpatterns = [
    path("<str:category>/", CategoryView.as_view(), name="category"),
]