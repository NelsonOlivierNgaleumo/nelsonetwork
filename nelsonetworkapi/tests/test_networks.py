from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from nelsonetworkapi.models import Network, User, Device
from nelsonetworkapi.views.network import NetworkSerializer


class NetworkTests(APITestCase):
    fixtures = ['devices', 'networks', 'users']

    def setUp(self):
        """Set up test dependencies."""
        self.user = User.objects.first()
        self.device = Device.objects.create(device_name="Test Device", device_ip="192.168.1.100", user=self.user)
        self.client.force_authenticate(user=self.user)  # Authenticate user for request

# Test to create a New Network
# run this command: python manage.py test nelsonetworkapi.tests.test_networks

    def test_create_network(self):
        """Test creating a new network."""
        # url = "/networks/"
        url = reverse("network-list")
        
        network_data = {
            "network_name": "Office Network",
            "network_type": "LAN",
            "number_of_staff": 15,
            "setup_recommendation": "Use VLAN segmentation",
            "network_ip_address": "192.168.1.1",
            "location": "Headquarters",
            "user_id": self.user.id,
            "device_id": self.device.device_id
        }

        response = self.client.post(url, network_data, format='json')
        
        print(f"Response Status Code: {response.status_code}")  # Debugging
        print(f"Response Data: {response.data}")  # Debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_network = Network.objects.last()
        expected = NetworkSerializer(new_network).data
        
        self.assertEqual(expected, response.data)

# Test to GET a Single Network
# run this command: python manage.py test nelsonetworkapi.tests.test_networks


    def test_get_networks(self):
        """ Get Network Test
        """
        network =Network.objects.first()
        
        url = f'/networks/{network.network_id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = NetworkSerializer(network)
        
        self.assertEqual(expected.data, response.data)

# Test to lIST all the Networks
# run this command: python manage.py test nelsonetworkapi.tests.test_networks

    def test_list_networks(self):
        """Test list networks
        """
        url = '/networks'
        
        response = self.client.get(url)
        
        all_networks = Network.objects.all()
        expected = NetworkSerializer(all_networks, many=True)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

# Test to UPDATE a Network
# run this command: python manage.py test nelsonetworkapi.tests.test_networks


    def test_change_network(self):
        """test update network
        """
        network = Network.objects.first()
        
        url = f'/networks/{network.network_id}'
        
        updated_network = {
            "network_name": "Office Network",
            "network_type": "LAN",
            "number_of_staff": 15,
            "setup_recommendation": "Use VLAN segmentation",
            "network_ip_address": "192.168.1.1",
            "location": "Headquarters",
            "user_id": self.user.id,
            "device_id": self.device.device_id
        }
        
        response = self.client.put(url, updated_network, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure update is successful

        # Refresh the network object to reflect any changes in the database
        network.refresh_from_db()

        # Assert that the updated values match
        self.assertEqual(updated_network["network_name"], network.network_name)
        self.assertEqual(updated_network["network_type"], network.network_type)
        self.assertEqual(updated_network["number_of_staff"], network.number_of_staff)
        self.assertEqual(updated_network["setup_recommendation"], network.setup_recommendation)
        self.assertEqual(updated_network["network_ip_address"], network.network_ip_address)  
        self.assertEqual(updated_network["location"], network.location) 
        self.assertEqual(updated_network["user_id"], network.user_id)
        self.assertEqual(updated_network["device_id"], network.device_id.pk) 

# Test to DELETE a Network
# run this command: python manage.py test nelsonetworkapi.tests.test_networks

    def test_delete_network(self):
        """Test delete tour
        """
        network = Network.objects.first()
        
        url = f'/networks/{network.network_id}'
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        response =self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
