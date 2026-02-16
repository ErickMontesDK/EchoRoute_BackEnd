from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

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