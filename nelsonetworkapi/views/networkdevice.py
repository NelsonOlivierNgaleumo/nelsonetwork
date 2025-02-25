from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from nelsonetworkapi.models import NetworkDevice, Network, Device


class NetworkDeviceView(ViewSet):
    """NetworkDevice API ViewSet"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single network-device relationship"""
        try:
            network_device = NetworkDevice.objects.get(pk=pk)
            serializer = NetworkDeviceSerializer(network_device)
            return Response(serializer.data)
        except NetworkDevice.DoesNotExist:
            return Response({'message': 'NetworkDevice not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to list all network-device relationships"""
        network_devices = NetworkDevice.objects.all()
        serializer = NetworkDeviceSerializer(network_devices, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new network-device relationship"""
        try:
            network = Network.objects.get(pk=request.data["network_id"])
            device = Device.objects.get(pk=request.data["device_id"])

            network_device = NetworkDevice.objects.create(
                network=network,
                device=device,
                status=request.data.get("status", "Pending")  # Default to 'Pending' if not provided
            )

            serializer = NetworkDeviceSerializer(network_device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"message": "Network or Device not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests to update a network-device relationship"""
        try:
            network_device = NetworkDevice.objects.get(pk=pk)

            # Update status if provided
            if "status" in request.data:
                network_device.status = request.data["status"]

            # Update Foreign Keys if provided
            if "network_id" in request.data:
                network_device.network = Network.objects.get(pk=request.data["network_id"])
            if "device_id" in request.data:
                network_device.device = Device.objects.get(pk=request.data["device_id"])

            network_device.save()
            serializer = NetworkDeviceSerializer(network_device)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except NetworkDevice.DoesNotExist:
            return Response({"message": "NetworkDevice not found"}, status=status.HTTP_404_NOT_FOUND)
        except Network.DoesNotExist:
            return Response({"message": "Network not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"message": "Device not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a network-device relationship"""
        try:
            network_device = NetworkDevice.objects.get(pk=pk)
            network_device.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except NetworkDevice.DoesNotExist:
            return Response({'message': 'NetworkDevice not found'}, status=status.HTTP_404_NOT_FOUND)


class NetworkDeviceSerializer(serializers.ModelSerializer):
    """JSON serializer for NetworkDevice"""
    class Meta:
        model = NetworkDevice
        fields = ['id', 'network', 'device', 'status']
        depth = 1  # To include related network and device details
