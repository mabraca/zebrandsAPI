from rest_framework import serializers
from .models import Product

"""
This serializer converts Product instances to JSON format, 
including only the specified fields: id, sku, name, price, brand, is_active, and visit_count.
"""


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'price', 'brand', 'is_active', 'visit_count']
