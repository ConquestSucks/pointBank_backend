from rest_framework import serializers
from .models import User, Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            login=validated_data['login'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['departure', 'arrival', 'from_location', 'to_location']


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)
