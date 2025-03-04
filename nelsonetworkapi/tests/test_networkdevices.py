from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from nelsonetworkapi.models import NetworkDevice, Network, Device, User
from nelsonetworkapi.views.networkdevice import NetworkDeviceSerializer

class NetworkDeviceTests(APITestCase):
    fixtures = ['devices', 'networks', 'users']  # Assuming these fixtures exist

    def setUp(self):
        """Set up test dependencies."""
        self.client = APIClient()

        # Get or create test data
        self.user = User.objects.first()
        self.network = Network.objects.first() or Network.objects.create(
            network_name="Test Network",
            network_type="LAN",
            network_ip_address="192.168.1.1",
            user_id=self.user.id
        )
        self.device = Device.objects.first() or Device.objects.create(
            device_name="Test Device",
            device_ip="192.168.1.100",
            user=self.user
        )

        # Create a NetworkDevice instance
        self.network_device = NetworkDevice.objects.create(
            network=self.network,
            device=self.device,
            status="Active"
        )
# Test to create a New NetworkDevice
# run this command: python manage.py test nelsonetworkapi.tests.test_networkdevices

    def test_create_network_device(self):
        """Test creating a new network-device relationship."""
        url = reverse("networkdevice-list")  # Assumes router basename='networkdevice'

        data = {
            "network_id": self.network.network_id,
            "device_id": self.device.device_id,
            "status": "Inactive"
        }

        response = self.client.post(url, data, format='json')

        print(f"Response Status Code: {response.status_code}")  # Debugging
        print(f"Response Data: {response.data}")  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_network_device = NetworkDevice.objects.last()
        expected = NetworkDeviceSerializer(new_network_device).data
        self.assertEqual(expected, response.data)

# Test to GET a SINGLE a NetworkDevice
# run this command: python manage.py test nelsonetworkapi.tests.test_networkdevices

    def test_get_network_device(self):
        """Test retrieving a single network-device relationship."""
        url = reverse("networkdevice-detail", kwargs={"pk": self.network_device.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected = NetworkDeviceSerializer(self.network_device).data
        self.assertEqual(expected, response.data)
