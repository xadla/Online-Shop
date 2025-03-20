from django.urls import path


from .views import AddItem, CartDetailView


app_name = "cart"
urlpatterns = [
    path("add/", AddItem.as_view(), name="add"),
    path('<int:id>/', CartDetailView.as_view(), name='cart-detail'),
]
