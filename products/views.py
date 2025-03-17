from django.shortcuts import render
from django.views import View


from .fetch import fetch
from .models import Product


class ProductsView(View):

    template_name = "products/products.html"

    def get(self, request):
        products = Product.objects.values("img_path")
        paths = [item['img_path'] for item in products]
        urls = fetch(paths)
        return render(request, self.template_name, {"urls": urls})