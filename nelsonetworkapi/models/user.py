from django.db import models

class User(models.Model):
  user_id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  email = models.EmailField()
  role = models.CharField(max_length=50)
