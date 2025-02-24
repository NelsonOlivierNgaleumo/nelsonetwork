from django.db import models
from .network import Network
from .device import Device

class NetworkDevice(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='networkdevices')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='devicenetworks')
    status = models.CharField(max_length=20, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Pending', 'Pending')
    ], default='Pending')
