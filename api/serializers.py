from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Client, Visit, ClientType, Route
from users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = f"{user.first_name} {user.last_name}"
        token['role'] = user.role
        token['username'] = user.username

        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class ClientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientType
        fields = ['name']

class ClientSerializer(serializers.ModelSerializer):
    client_type = ClientTypeSerializer(read_only=True, source='client_type')

    class Meta:
        model = Client
        fields = ['code', 'name', 'client_type', 'address', 'neighborhood', 'municipality', 'state', 'latitude', 'longitude', 'sector', 'market']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'role']

class VisitSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    deliverer_details = UserSerializer(source='deliverer', read_only=True)

    class Meta:
        model = Visit
        fields = [
            'id', 
            'client',
            'deliverer',
            'client_details', 
            'deliverer_details', 
            'visited_at', 
            'latitude_recorded', 
            'longitude_recorded',
            'is_productive', 
            'is_valid', 
            'notes'
        ]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'name', 'deliverer', 'day_of_week']
