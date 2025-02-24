from django.db import models
from .device import Device


class Documentation(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=50)
    configuration = models.TextField()
