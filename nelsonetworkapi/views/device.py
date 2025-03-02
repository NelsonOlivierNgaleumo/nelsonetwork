from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from nelsonetworkapi.models import Device, User


class DeviceView(ViewSet):
    """Device API ViewSet"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single device"""
        try:
            device = Device.objects.get(device_id=pk)  
            serializer = DeviceSerializer(device)
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response({'message': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to list all devices"""
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new device"""
        try:
            user = User.objects.get(pk=request.data["user_id"])  # Validate user

            device = Device.objects.create(
                device_name=request.data["device_name"],
                device_image=request.data["device_image"],
                age_of_device=request.data["age_of_device"],
                device_ip=request.data["device_ip"],
                device_type=request.data["device_type"],
                device_description=request.data["device_description"],
                serial_number=request.data["serial_number"],
                mac_address=request.data["mac_address"],
                location=request.data["location"],
                user=user,
                last_software_update=request.data["last_software_update"]
            )

            serializer = DeviceSerializer(device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests to update a device"""
        try:
            device = Device.objects.get(pk=pk) 

            # Update fields (only if provided)
            device.device_name = request.data.get("device_name", device.device_name)
            device.device_image = request.data.get("device_image", device.device_image)
            device.age_of_device = request.data.get("age_of_device", device.age_of_device)
            device.device_ip = request.data.get("device_ip", device.device_ip)
            device.device_type = request.data.get("device_type", device.device_type)
            device.device_description = request.data.get("device_description", device.device_description)
            device.serial_number = request.data.get("serial_number", device.serial_number)
            device.mac_address = request.data.get("mac_address", device.mac_address)
            device.location = request.data.get("location", device.location)
            device.last_software_update = request.data.get("last_software_update", device.last_software_update)

            # Handle Foreign Key updates
            if "user_id" in request.data:
                device.user = User.objects.get(pk=request.data["user_id"])

            device.save()
            serializer = DeviceSerializer(device)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Device.DoesNotExist:
            return Response({"message": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a device"""
        try:
            device = Device.objects.get(pk=pk) 
            device.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Device.DoesNotExist:
            return Response({'message': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)


class DeviceSerializer(serializers.ModelSerializer):
    """JSON serializer for devices"""
    class Meta:
        model = Device
        fields = ['device_id', 'device_name', 'device_image', 'age_of_device',
                  'device_ip', 'device_type', 'device_description',
                  'serial_number', 'mac_address', 'location', 'user',
                  'last_software_update']
        depth = 1  # To include related User details
