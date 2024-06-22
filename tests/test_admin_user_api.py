from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AdminUserAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword',
                                                        email='zebrandsApiTest@yopmail.com', first_name="First", last_name="Test", is_superuser=True)
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.other_admin_user = User.objects.create_user(username='otheradminuser', password='otheradminuser', first_name="Second", last_name="Test",
                                                         email='zebrandsApiTest2@yopmail.com', is_superuser=True)
        self.url_create = reverse('admin-add')
        self.url_update = reverse('admin-edit', kwargs={'pk': self.other_admin_user.pk})
        self.url_delete = reverse('admin-delete', kwargs={'pk': self.other_admin_user.pk})

    def test_create_admin_user(self):
        response = self.client.post(self.url_create, {'username': 'newadmin', 'password': 'newadminpassword',
                                                      'first_name': 'Third', 'last_name': 'Test',
                                                      'email': 'zebrandsApiTest3@yopmail.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_update_admin_user(self):
        response = self.client.put(self.url_update, {'first_name': 'updateduser', 'password': 'updatedpassword'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.other_admin_user.refresh_from_db()
        self.assertEqual(self.other_admin_user.first_name, 'updateduser')

    def test_delete_admin_user(self):
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
