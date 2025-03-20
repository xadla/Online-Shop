from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Cart
from .serializers import ItemSerializer, CartSerializer


class AddItem(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                cart, _ = Cart.objects.get_or_create(user=request.user)

                serializer.save(cart=cart)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            session = request.session
            if "cart" not in session:
                session["cart"] = []

            product_id = request.data.get("product")
            existing_item = next((item for item in session["cart"] if item["product"] == product_id), None)

            if existing_item:
                existing_item["quantity"] += request.data.get("quantity", 1)
            else:
                session["cart"].append(request.data)

            session.modified = True

            return Response({"message": "Item added to session cart!"}, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):

    def get(self, request, id):
        try:
            cart = Cart.objects.get(id=id)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)

