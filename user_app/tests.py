from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth.models import User


class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password': 'pass1234',
            'password2':'pass1234'
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testcase')

class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="pass1234")
    
    def test_login(self):
        data = {
            'username': 'example',
            'password': 'pass1234',
        }
        url = reverse('login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


