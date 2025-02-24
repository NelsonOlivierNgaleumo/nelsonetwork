"""View module for handling requests about users"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.hashers import make_password
from nelsonetworkapi.models import User


class UserView(ViewSet):
    """User view"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single user"""
        try:
            nn_user = User.objects.get(user_id=pk)  # Use `user_id` as primary key
            serializer = UserSerializer(nn_user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to retrieve all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)  

    def create(self, request):
        """Handle POST operations for creating a user"""
        try:
            nn_user = User.objects.create(
                username=request.data["username"],
                password=make_password(request.data["password"]),  # Hash password
                email=request.data["email"],
                role=request.data.get("role", "user")  # Default role if not provided
            )
            serializer = UserSerializer(nn_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response(
                {"message": f"Missing required field: {e.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        """Handle PUT requests for updating a user"""
        try:
            nn_user = User.objects.get(user_id=pk)

            # Update fields (ensuring field names match the model)
            nn_user.username = request.data.get("username", nn_user.username)
            if "password" in request.data:
                nn_user.password = make_password(request.data["password"])  # Secure password update
            nn_user.email = request.data.get("email", nn_user.email)
            nn_user.role = request.data.get("role", nn_user.role)
            nn_user.save()

            serializer = UserSerializer(nn_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except KeyError as e:
            return Response(
                {"message": f"Missing required field: {e.args[0]}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a user"""
        try:
            nn_user = User.objects.get(user_id=pk)
            nn_user.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'role']
