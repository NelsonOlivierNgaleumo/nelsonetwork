from django.db import models
from .network import Network
from .user import User


class Device(models.Model):
  
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=100)
    device_image = models.URLField()
    age_of_device = models.CharField(max_length=50)
    device_ip = models.GenericIPAddressField()
    device_type = models.CharField(max_length=50)
    device_description = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_software_update = models.CharField(max_length=50)
