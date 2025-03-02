from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from nelsonetworkapi.models import User, Device
from nelsonetworkapi.views.device import DeviceSerializer


class DeviceTests(APITestCase):
    fixtures = ['devices', 'users']
    
    def setUp(self):
      """Set up test dependencies."""
      self.user = User.objects.first()

# Test to create a New Device
# run this command: python manage.py test nelsonetworkapi.tests.test_devices

    def test_create_device(self):
        """Test creating a new device."""
        url = reverse("device-list")
        
        device_data = {
        # {
        #     "device_name": "Test Router",
        #     "device_image": "http://example.com/image.jpg",
        #     "age_of_device": "2 years",
        #     "device_ip": "192.168.1.10",
        #     "device_type": "Router",
        #     "device_description": "A test router for networking",
        #     "serial_number": "ABC12345",
        #     "mac_address": "00:1A:2B:3C:4D:5E",
        #     "location": "Data Center",
        #     "user_id": self.user.id,
        #     "last_software_update": "2024-01-10"
        # },
        
      "device_name": "Tempsoft",
      "device_image": "http://dummyimage.com/205x100.png/dddddd/000000",
      "age_of_device": "70-269-5107",
      "device_ip": "78.11.208.227",
      "device_type": "Aerified",
      "device_description": "fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in",
      "serial_number": "XYZ98765",
      "mac_address": "65-0F-57-E2-E5-C0",
      "location": "Suite 45",
      "user_id": self.user.id,
      "last_software_update": "7/7/2024"
    }

        response = self.client.post(url, device_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_device = Device.objects.last()
        expected = DeviceSerializer(new_device).data
        
        self.assertEqual(expected, response.data)      
      
      
# Test to GET A SINGLE Device
# run this command: python manage.py test nelsonetworkapi.tests.test_devices

    def test_get_device(self):
        """Test retrieving a single device."""
        device = Device.objects.first()
        url = f'/devices/{device.device_id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = DeviceSerializer(device)
        
        self.assertEqual(expected.data, response.data)

# Test to LIST ALL Device
# run this command: python manage.py test nelsonetworkapi.tests.test_devices

    def test_list_devices(self):
        """Test listing all devices."""
        
        url = '/devices'
        
        response = self.client.get(url)
        
        all_devices = Device.objects.all()
        expected = DeviceSerializer(all_devices, many=True).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.data)

# Test to UPDATE A Device
# run this command: python manage.py test nelsonetworkapi.tests.test_devices    

    def test_update_device(self):
        """Test updating a device."""
        device = Device.objects.first()
        url = f'/devices/{device.device_id}'
        
        updated_data = {
      "device_name": "Tempsoft",
      "device_image": "http://dummyimage.com/205x100.png/dddddd/000000",
      "age_of_device": "70-269-5107",
      "device_ip": "78.11.208.227",
      "device_type": "Aerified",
      "device_description": "fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in",
      "serial_number": "XYZ98765",
      "mac_address": "65-0F-57-E2-E5-C0",
      "location": "Suite 45",
      "user_id": self.user.id,
      "last_software_update": "7/7/2024"
        }
        
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        device.refresh_from_db()
        
        self.assertEqual(device.device_name, updated_data["device_name"])
        self.assertEqual(device.device_image, updated_data["device_image"])
        self.assertEqual(device.age_of_device, updated_data["age_of_device"])
        self.assertEqual(device.device_ip, updated_data["device_ip"])
        self.assertEqual(device.device_type, updated_data["device_type"])
        self.assertEqual(device.device_description, updated_data["device_description"])
        self.assertEqual(device.serial_number, updated_data["serial_number"])
        self.assertEqual(device.mac_address, updated_data["mac_address"])
        self.assertEqual(device.location, updated_data["location"])
        self.assertEqual(device.user.id, updated_data["user_id"])
        self.assertEqual(device.last_software_update, updated_data["last_software_update"])

# Test to DELETE A Device
# run this command: python manage.py test nelsonetworkapi.tests.test_devices    

    def test_delete_device(self):
        """Test deleting a device."""
        device = Device.objects.first()
        url = f'/devices/{device.device_id}'
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        response = self.client.get(url)
