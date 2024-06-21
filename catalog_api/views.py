from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Product, Log
from .serializers import ProductSerializer

"""
Class ProductListCreateAPIView manage product list and create products
Permission class ensures that only authenticated users can create, update or delete products, while anyone can see them.
"""


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Save the new product instance when it's create
        serializer.save()

    def get_queryset(self):
        # Override the default get_queryset method to allow searching by name or all if query params doesn't exits
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        # Override the list method to use the custom get_queryset method
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
Class ProductDetailAPIView manage the detail of a product
"""


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
