from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from catalog_api.models import Product


class ProductListCreateAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword',
                                                        is_superuser=True)
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product_data = {'name': 'Test Product', 'price': 10.0, 'brand': 'Test Brand', 'sku': '123456'}
        self.url = reverse('product-get-post')

    def test_list_products(self):
        Product.objects.create(name='Test Product', price=10.0, brand='Test Brand', sku='123456')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_product_authenticated(self):
        response = self.client.post(self.url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_create_product_unauthenticated(self):
        self.client.credentials()  # Remove token
        response = self.client.post(self.url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
