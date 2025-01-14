from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class CustomerRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    age = serializers.IntegerField(required=True)
    first_name = serializers.CharField(max_length=255,required=True)
    last_name = serializers.CharField(max_length=255,required=True)
    address = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age', 'address', 'phone']

    def create(self, validated_data):
        age = validated_data.pop('age')
        address = validated_data.pop('address')
        phone = validated_data.pop('phone')

        # Tạo người dùng
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )

        # Tìm hoặc tạo role
        role, _ = Role.objects.get_or_create(role_name="Customer")

        # Tạo Shipper profile (hoặc bất kỳ role liên quan)
        Customer.objects.create(
            user=user,
            age=age,
            address=address,
            phone=phone
        )
        return user




