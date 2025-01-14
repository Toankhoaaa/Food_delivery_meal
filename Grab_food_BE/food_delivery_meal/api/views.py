from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer
from .serializers import LoginSerializer, CustomerRegistrationSerializer


def home(request):
    return HttpResponse("Hello, Django!")


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                # Tạo token JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({
                    'message': 'Login successful',
                    'access_token': access_token
                }, status=200)
            else:
                return Response({'message': 'Invalid credentials'}, status=400)
        return Response(serializer.errors, status=400)

class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Shipper account created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)