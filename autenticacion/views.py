from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
User = get_user_model()
from datetime import datetime



class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kargs):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            user.last_login = datetime.now()
            user.save()
            refresh = RefreshToken.for_user(user)
            user = UserSerializer(instance=user)
            response = {
                'success': True,
                "user": user.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "username": {
                "detail": "No se pudo validar el usuario."
            }
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            if self.request.data.get('is_admin', False):
                self.permission_classes = [IsAdminUser]
                self.authentication_classes = [JWTAuthentication]
            else:
                self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def post(self, request, *args, **kwargs):
        is_admin = request.data.get('is_admin', False)
        if is_admin:
            if not request.user.is_admin:
                return Response({"detail": "No tiene permisos para crear un usuario administrador."},
                                status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            authenticate(email=request.data['email'], password=request.data['password'])
            response = {
                'success': True,
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)


class ExampleView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        user, created = User.objects.get_or_create(email=request.data['email'], name=request.data['name'])
        user.last_login = datetime.now()
        user.save()
        refresh = RefreshToken.for_user(user)
        user = UserSerializer(instance=user)
        response = {
            'success': True,
            "user": user.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response, status=status.HTTP_201_CREATED) if created else Response(response, status=status.HTTP_200_OK)
