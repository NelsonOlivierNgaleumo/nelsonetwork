from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from nelsonetworkapi.models import User
from nelsonetworkapi.views.user import UserSerializer


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
        expected = UserSerializer(new_user).data
        
        self.assertEqual(expected, response.data)

    # Test retrieving a single user
    # run this command: python manage.py test nelsonetworkapi.tests.test_users
    
    def test_get_user(self):
        """Test retrieving a single user."""
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = UserSerializer(self.user).data
        self.assertEqual(expected, response.data)

# Test listing all users
# run this command: python manage.py test nelsonetworkapi.tests.test_users
    
    def test_list_users(self):
        """Test listing all users."""
        url = reverse("user-list")
        response = self.client.get(url)
        
        all_users = User.objects.all()
        expected = UserSerializer(all_users, many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.data)
        
    # Test to UPDATE a user
    # run this command: python manage.py test nelsonetworkapi.tests.test_users
    
    def test_update_user(self):
        """Test updating a user."""
        url = reverse("user-detail", args=[self.user.id])
        updated_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newpassword",
            "role": "user"
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_data["username"])
        self.assertEqual(self.user.email, updated_data["email"])
        self.assertEqual(self.user.role, updated_data["role"])
    