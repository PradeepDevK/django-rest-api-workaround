from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password': 'testcase@123',
            'password2': 'testcase@123'
        }
        url = reverse('register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testcase1',
            password='testcase@123'
        )
    def test_login(self):
        data = {
            'username': 'testcase1',
            'password': 'testcase@123'
        }
        url = reverse('login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.token = Token.objects.get(user__username="testcase1")
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        