from django.db import models
from .user import User

class Network(models.Model):
    
    network_id = models.AutoField(primary_key=True)
    network_name = models.CharField(max_length=100)
    network_type = models.CharField(max_length=50)
    number_of_staff = models.IntegerField()
    setup_recommendation = models.CharField(max_length=200)
    network_ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    device_id = models.ForeignKey('Device', on_delete=models.CASCADE)
