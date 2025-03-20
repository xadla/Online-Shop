from rest_framework import serializers


from products.models import Product
from .models import CartItem, Cart


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid product ID.")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
