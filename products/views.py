from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import Http404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from utils import fetch
from .models import Product
from .serializers import ProductSerializer


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
    

    def dispatch(self, request, *args, **kwargs):
        category = kwargs["category"]
        if category != "men" and category != "women" and category != "kids" and category != "beauty":
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class ProductView(View):

    template_name = "products/product.html"

    def get(self, request, id):

        product = get_object_or_404(Product, pk=id)
        url = fetch([product.img_path])
        return render(request, self.template_name, {"product": product, "url": url[0]})


class ProductAPI(APIView):

    def get(self, request):
        
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)
        data = serializers.data
        urls = fetch([d["img_path"] for d in data])
        for i in range(len(urls)):
            data[i]["img_path"] = urls[i]

        return Response(serializers.data, status=status.HTTP_200_OK)
