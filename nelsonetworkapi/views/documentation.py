from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from nelsonetworkapi.models import Documentation, Device


class DocumentationView(ViewSet):
    """API ViewSet for managing device documentation"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single documentation entry"""
        try:
            documentation = Documentation.objects.get(pk=pk)
            serializer = DocumentationSerializer(documentation)
            return Response(serializer.data)
        except Documentation.DoesNotExist:
            return Response({'message': 'Documentation not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to list all documentation entries"""
        documentation = Documentation.objects.all()
        serializer = DocumentationSerializer(documentation, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new documentation entry"""
        try:
            device = Device.objects.get(device_name=request.data["device_name"])

            documentation = Documentation.objects.create(
                device_name=device,
                device_type=request.data["device_type"],
                configuration=request.data["configuration"]
            )

            serializer = DocumentationSerializer(documentation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"message": f"Missing required field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
        except Device.DoesNotExist:
            return Response({"message": "Device not found"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests to update a documentation entry"""
        try:
            documentation = Documentation.objects.get(pk=pk)

            # Update ForeignKey if provided
            if "device_name" in request.data:
                documentation.device_name = Device.objects.get(device_name=request.data["device_name"])

            # Update fields if provided
            if "device_type" in request.data:
                documentation.device_type = request.data["device_type"]
            if "configuration" in request.data:
                documentation.configuration = request.data["configuration"]

            documentation.save()
            serializer = DocumentationSerializer(documentation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Documentation.DoesNotExist:
            return Response({"message": "Documentation not found"}, status=status.HTTP_404_NOT_FOUND)
        except Device.DoesNotExist:
            return Response({"message": "Device not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a documentation entry"""
        try:
            documentation = Documentation.objects.get(pk=pk)
            documentation.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Documentation.DoesNotExist:
            return Response({'message': 'Documentation not found'}, status=status.HTTP_404_NOT_FOUND)


class DocumentationSerializer(serializers.ModelSerializer):
    """JSON serializer for Documentation"""
    class Meta:
        model = Documentation
        fields = ['id', 'device_name', 'device_type', 'configuration']
        depth = 1  # To include related device details
