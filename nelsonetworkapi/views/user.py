"""View module for handling requests about users"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.hashers import make_password, check_password
from nelsonetworkapi.models import User


class UserView(ViewSet):
    """User ViewSet for CRUD operations"""

    def list(self, request):
        """GET all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET a single user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """POST create a new user"""
        data = request.data.copy()
        data['password'] = make_password(data['password'])  # Hash password before saving
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT update a user"""
        try:
            user = User.objects.get(pk=pk)
            data = request.data.copy()
            
            if 'password' in data:
                data['password'] = make_password(data['password'])  # Hash password before saving

            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """DELETE a user"""
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        
    def create(self, validated_data):
            """Override to hash the password before saving"""
            user = User(**validated_data)
            user.password = make_password(validated_data['password'])  # Hash password
            user.save()
            return user
