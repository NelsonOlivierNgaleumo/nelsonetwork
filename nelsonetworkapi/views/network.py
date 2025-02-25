from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from nelsonetworkapi.models import Network, User, Device


class NetworkView(ViewSet):
    """Network API ViewSet"""

    def retrieve(self, request, pk):
        """Handle GET request for a single network"""
        try:
            network = Network.objects.get(network_id=pk)
            serializer = NetworkSerializer(network)
            return Response(serializer.data)
        except Network.DoesNotExist:
            return Response({'message': 'Network not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET request to list all networks"""
        networks = Network.objects.all()
        serializer = NetworkSerializer(networks, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST request to create a new network"""
        try:
            user = User.objects.get(pk=request.data["user_id"])  # Validate user
            device = Device.objects.get(pk=request.data["device_id"])  # Validate device

            network = Network.objects.create(
                network_name=request.data["network_name"],
                network_type=request.data["network_type"],
                number_of_staff=request.data["number_of_staff"],
                setup_recommendation=request.data["setup_recommendation"],
                network_ip_address=request.data["network_ip_address"],
                user=user,
                location=request.data["location"],
                device_id=device
            )

            serializer = NetworkSerializer(network)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"message": "Device not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT request to update a network"""
        try:
            network = Network.objects.get(network_id=pk)

            # Update fields (only if provided)
            network.network_name = request.data.get("network_name", network.network_name)
            network.network_type = request.data.get("network_type", network.network_type)
            network.number_of_staff = request.data.get("number_of_staff", network.number_of_staff)
            network.setup_recommendation = request.data.get("setup_recommendation", network.setup_recommendation)
            network.network_ip_address = request.data.get("network_ip_address", network.network_ip_address)
            network.location = request.data.get("location", network.location)

            # Handle Foreign Key updates
            if "user_id" in request.data:
                network.user = User.objects.get(pk=request.data["user_id"])
            if "device_id" in request.data:
                network.device_id = Device.objects.get(pk=request.data["device_id"])

            network.save()
            serializer = NetworkSerializer(network)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Network.DoesNotExist:
            return Response({"message": "Network not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"message": "Device not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE request to delete a network"""
        try:
            network = Network.objects.get(network_id=pk)
            network.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Network.DoesNotExist:
            return Response({'message': 'Network not found'}, status=status.HTTP_404_NOT_FOUND)


class NetworkSerializer(serializers.ModelSerializer):
    """JSON serializer for networks"""
    class Meta:
        model = Network
        fields = ['network_id', 'network_name', 'network_type', 'number_of_staff',
                  'setup_recommendation', 'network_ip_address', 'user', 'location', 'device_id']
        depth = 1  # To include related User and Device details
