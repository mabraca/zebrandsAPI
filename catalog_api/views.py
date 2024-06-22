from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Log
from .serializers import ProductSerializer, AdminUserSerializerUpdate, AdminUserSerializerCreate

"""
Class ProductListCreateAPIView calls serializers to get, update and create products
Permission class ensures that only authenticated users can create, update or delete products, while anyone can see them.
"""


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        product = serializer.save(modified_by=self.request.user)
        self.create_log(product, created=True)

    def perform_update(self, serializer):
        product = serializer.save(modified_by=self.request.user)
        self.create_log(product, created=False)

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

    def create_log(self, product, created):
        current_user = self.request.user
        if created:
            action = Log.ADD
            action_text = f"Added: {product.name}, Price: {product.price}, Brand: {product.brand}, Active: {product.is_active}"
        else:
            action = Log.UPDATED
            action_text = f"Updated: {product.name}, Price: {product.price}, Brand: {product.brand}, Active: {product.is_active}"

        Log.objects.create(
            product=product,
            user=current_user,
            action=action,
            changes=action_text,
        )


"""
Class ProductDetailAPIView calls serializer for detail of a product
"""


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.visit_count += 1
        instance.save(update_fields=['visit_count'])
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=request.user)
        return Response(serializer.data)


"""
Class AdminUserCreateView calls serializer for create a product
"""


class AdminUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializerCreate
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'pk': serializer.instance.pk,
            'first_name': serializer.instance.first_name,
            'last_name': serializer.instance.last_name,
            'email': serializer.instance.email,
            'username': serializer.instance.username,
        }, status=status.HTTP_201_CREATED, headers=headers)


"""
Class AdminUserUpdateView calls serializer for update a product
"""


class AdminUserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializerUpdate
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


"""
Class AdminUserDeleteView delete a product in database
"""


class AdminUserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


"""
Class LoginView manage login generating token for request
"""


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
