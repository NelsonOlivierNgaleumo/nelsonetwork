from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from nelsonetworkapi.models import User
from nelsonetworkapi.views.user import UserSerializer
# from django.contrib.auth.hashers import check_password


class UserTests(APITestCase):
    fixtures = ['users']
    
    def setUp(self):
        """Set up test dependencies."""
        self.user = User.objects.first()
    
    # Test creating a new user
    # run this command: python manage.py test nelsonetworkapi.tests.test_users
    def test_create_user(self):
        """Test creating a new user."""
        url = reverse("user-list")
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword",
            "role": "admin"
        }
        
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        new_user = User.objects.get(username="testuser")
        # self.assertTrue(check_password("securepassword", new_user.password))
        expected = UserSerializer(new_user).data
        
        self.assertEqual(expected, response.data)
