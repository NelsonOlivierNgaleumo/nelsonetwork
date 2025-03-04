from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from nelsonetworkapi.models import User, Device, Documentation

class DocumentationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.device = Device.objects.create(
            device_name="Test Device",
            device_ip="192.168.1.100",
            user=self.user
        )
        self.documentation = Documentation.objects.create(
            device=self.device,
            device_type="Router",
            configuration="interface eth0\n ip address 192.168.1.1"
        )

# Test to create a New Documentation
# run this command: python manage.py test nelsonetworkapi.tests.test_documentations

    def test_create_documentation(self):
        """Test creating a new Documentation instance via API."""
        url = reverse("documentation-list")  # Assumes basename='documentation'
        data = {
            "device_id": self.device.device_id, 
            "device_type": "Switch",
            "configuration": "vlan 10\n name VLAN_TEST"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["device_type"], "Switch")

# Test to GET a SINGLE Documentation
# run this command: python manage.py test nelsonetworkapi.tests.test_documentations

    def test_get_documentation(self):
        """Test retrieving a single Documentation instance."""
        url = reverse("documentation-detail", kwargs={"pk": self.documentation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["device_type"], "Router")

# Test to LIST all Documentation
# run this command: python manage.py test nelsonetworkapi.tests.test_documentations

    def test_list_documentation(self):
        """Test listing all Documentation instances."""
        url = reverse("documentation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

# Test to UPDATE AND DELETE Documentation
# run this command: python manage.py test nelsonetworkapi.tests.test_documentations

    def test_update_documentation(self):
        """Test updating a Documentation instance via API."""
        url = reverse("documentation-detail", kwargs={"pk": self.documentation.id})
        data = {
            "device_id": self.device.pk,
            "device_type": "Firewall",
            "configuration": "rule 1 permit ip any any"
        }
        response = self.client.put(url, data, format='json')
        print(f"Update Response Status Code: {response.status_code}")
        print(f"Update Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["device_type"], "Firewall")

    def test_delete_documentation(self):
        """Test deleting a Documentation instance."""
        url = reverse("documentation-detail", kwargs={"pk": self.documentation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify deletion
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
