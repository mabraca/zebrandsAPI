from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Product

"""
Theses serializers make all the logic to Create, Update, Delete products and user admins 
"""


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'price', 'brand', 'is_active', 'visit_count']


class AdminUserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        admin_group, created = Group.objects.get_or_create(name='Admins')

        user_permissions = Permission.objects.filter(content_type__app_label='auth',
                                                     codename__in=['add_user', 'update_user', 'delete_user'])

        for permission in user_permissions:
            admin_group.permissions.add(permission)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.groups.add(admin_group)

        return user


class AdminUserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'read_only': True, 'required': False},
        }

    def update(self, instance, validated_data):
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']

        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']

        if 'email' in validated_data:
            instance.email = validated_data['email']

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
