# Welcome to NelsoNetwork App Server

Nelsonetwork is a web application designed to manage networks, devices, and their relationships. This app enables users to maintain detailed records of networks, devices, and associated user information while also providing the flexibility to manage many-to-many relationships between networks and devices.

This repository houses the backend server for Nelsonetwork App  

Click on the following Link to the [API Documentation](https://documenter.getpostman.com/view/35134770/2sAYdhHVGZ)

# Getting Started
- Fork this repo  
- Clone repo to your machine using "*git clone https://github.com/NelsonOlivierNgaleumo/nelsonetwork.git*"    
- Navigate to project directory *cd nelsonetwork* 
- Activate the Pipenv environment with *pipenv shell*  
- Install the dependencies using *pipenv install*  
- Open the project in Visual Studio Code  
- Ensure that the correct interpreter is selected  
- Run *python manage.py runserver* to start the server

# About the User  
- The perfect User for this Application is a Network Engineer/Administrator, Small Business Manager, Network Engineering Student/Enthusiast.
- The User wants to create a network/ subnetwork for his business  
- The User wants to add various devices to that network he just created for his business  
- The User wants to Check all the devices present in a network, know when to perform system updates and maintainance  

# Features
- *Network Management*: Create and manage network configurations, including network name, type, IP address, and staff size. Perform CRUD operations on network.  
- *Device Management*: Add and manage devices, including attributes like device name, IP address, type, serial number, and location. Perform CRUD operations on device.  
- *Documentation*: Maintain documentation for devices, including configuration settings and device-specific details. Perform CRUD operations on documentation.  
- *User Management*: Manage users with roles and access permissions. Perform CRUD operations on users.  
- *Network-Device Relationship*: Establish and manage a many-to-many relationship between networks and devices. Perform CRUD operations on networkdevices.

# Models
- *Device*: Represents a device with attributes such as device name, IP address, description, and more. Devices are associated with users.
- *Documentation*: Contains configuration and device-type-specific documentation for each device.
- *Network*: Represents a network, including network name, type, and IP address. Networks are associated with users and devices.
- *NetworkDevice*: A join model for managing the many-to-many relationship between networks and devices. It includes a status field to track whether a device is Active, Inactive, or Pending in a network.
- *User*: Represents a user with attributes such as username, password, email, and role.

# Endpoints
- network: List, create, and edit networks.
- device: List, create, and edit devices.
- documentation: Manage device documentation and configurations.
- user: Manage users, their roles, and permissions.
- network-device: Manage the relationships between networks and devices, including setting device status.
  

# Video Walkthrough of Nelsonetwork Django Server 
[Loom Video Walkthrough](www.loom.com/share/34fc5b416aa44e7eab0c59d4b2030c4d)

# Interesting Links
- [API Documentation Link](https://documenter.getpostman.com/view/35134770/2sAYdhHVGZ)  
- Entity Relationship Diagram, [ERD Link](https://dbdiagram.io/d/NELSONETWORK-67a8e9ce263d6cf9a08915e6)
- Video for Endpoints Display on Postman [Postman Video Link](https://www.loom.com/share/34fc5b416aa44e7eab0c59d4b2030c4d), [Videolink2](https://www.loom.com/share/6fb4c220f97f4264b96229a9a04e626c), [Videolink3](https://www.loom.com/share/bea8048d421a450995111fea1aed083a)
- Integration tests for CRUD operations on all entities (network, device, documentation, networkdevices) [Integration Tests Video](https://www.loom.com/share/4eb2043f318342bfb15fccc5f5658c2b)

# [Project Board](https://github.com/users/NelsonOlivierNgaleumo/projects/1)  

# Code Snippet

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


# Contributors
- Nelson Ngaleumo (https://github.com/NelsonOlivierNgaleumo)




