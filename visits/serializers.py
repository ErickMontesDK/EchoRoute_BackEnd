from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Client, Visit, ClientType, Route
from users.models import User
from math import radians, sin, asin, sqrt, cos


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
        try:
            data = super().validate(attrs)
            print("Token refresh successful")
            return data
        except Exception as e:
            print(f"Token refresh failed: {str(e)}")
            raise e

class ClientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientType
        fields = ['name']

class ClientSerializer(serializers.ModelSerializer):
    client_type = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Client
        fields = ['id', 'code', 'name', "client_type", 'address', 'neighborhood', 'municipality', 'state', 'latitude', 'longitude', 'sector', 'market']

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

    def validate(self, data):
        client = data.get('client')
        lat_scan = data.get('latitude_recorded')
        lng_scan = data.get('longitude_recorded')


        if client and lat_scan and lng_scan:
            client_lat = client.latitude
            client_lng = client.longitude

            # Earth radius in meters (IUGG mean radius: 6371008.8 m)
            earth_radius = 6371008.8
            
            # Ensure coordinates are floats for precision calculation
            lat1, lon1 = map(radians, [float(client_lat), float(client_lng)])
            lat2, lon2 = map(radians, [float(lat_scan), float(lng_scan)])
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * asin(sqrt(a))
            distance = earth_radius * c

            print(f"Calculated distance: {distance} meters")
            data['distance_from_client'] = distance

            # Validity check (e.g., within 100 meters)
            data['is_valid'] = distance < 100
            
        return data


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'name', 'deliverer', 'day_of_week']
