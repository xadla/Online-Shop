from django.shortcuts import render
from django.views import View


from .fetch import fetch
from .models import Product


class CategoryView(View):
    template_name = "products/category.html"

    def get(self, request, category):
        products = Product.objects.filter(category=category)
        urls = fetch([product.img_path for product in products])

        products_with_urls = [
            {"product": product, "url": url}
            for product, url in zip(products, urls)
        ]

        return render(request, self.template_name, {"products_with_urls": products_with_urls})