from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from catalog_api.models import Product


class ProductDetailAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword', is_superuser=True)
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product = Product.objects.create(name='Test Product', price=10.0, brand='Test Brand', sku='123456')
        self.url = reverse('product-get-put', kwargs={'pk': self.product.pk})

    def test_retrieve_count_visited_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.visit_count, 1)

    def test_update_product_authenticated(self):
        response = self.client.put(self.url, {'name': 'Updated Product', 'price': 15.0, 'brand': 'Updated Brand'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_update_product_unauthenticated(self):
        self.client.credentials()
        response = self.client.put(self.url, {'name': 'Updated Product', 'price': 15.0, 'brand': 'Updated Brand'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
