import cloudinary.uploader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.parsers import MultiPartParser
import cloudinary
from .models import *
from .serializers import *


class HomeTextView(ModelViewSet):
    """
    Vista para el Texto de la Home
    """

    serializer_class = HomeTextSerializer
    queryset = HomeText.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class HomeStartImageView(ModelViewSet):
    """
    Vista para las Imágenes de la Sección Inicio de la Home
    """

    serializer_class = HomeStartImageSerializer
    queryset = HomeStartImage.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cloudinary.uploader.destroy(
            instance.start_image.public_id, invalidate=True
        )  # Borrar la vieja imagen en Cloudinary
        self.perform_destroy(instance)  # Borrar la vieja imagen
        self.perform_create(serializer)  # serializer.save() Guardar la nueva imagen
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cloudinary.uploader.destroy(instance.start_image.public_id, invalidate=True)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomeCombinationsImageView(ModelViewSet):
    """
    Vista para las Imágenes de la Sección Combinaciones de la Home
    """

    serializer_class = HomeCombinationsImageSerializer
    queryset = HomeCombinationsImage.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cloudinary.uploader.destroy(
            instance.combinations_image.public_id, invalidate=True
        )  # Borrar la vieja imagen en Cloudinary
        self.perform_destroy(instance)  # Borrar la vieja imagen
        self.perform_create(serializer)  # serializer.save() Guardar la nueva imagen
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cloudinary.uploader.destroy(
            instance.combinations_image.public_id, invalidate=True
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomeProductsImageView(ModelViewSet):
    """
    Vista para las Imágenes de la Sección Productos de la Home
    """

    serializer_class = HomeProductsImageSerializer
    queryset = HomeProductsImage.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cloudinary.uploader.destroy(
            instance.products_image.public_id, invalidate=True
        )  # Borrar la vieja imagen en Cloudinary
        self.perform_destroy(instance)  # Borrar la vieja imagen
        self.perform_create(serializer)  # serializer.save() Guardar la nueva imagen
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cloudinary.uploader.destroy(instance.products_image.public_id, invalidate=True)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomeAlliesImageView(ModelViewSet):
    """
    Vista para las Imágenes de la Sección Aliados de la Home
    """

    serializer_class = HomeAlliesImageSerializer
    queryset = HomeAlliesImage.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cloudinary.uploader.destroy(
            instance.allies_image.public_id, invalidate=True
        )  # Borrar la vieja imagen en Cloudinary
        self.perform_destroy(instance)  # Borrar la vieja imagen
        self.perform_create(serializer)  # serializer.save() Guardar la nueva imagen
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cloudinary.uploader.destroy(instance.allies_image.public_id, invalidate=True)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InfoBarView(ModelViewSet):
    """
    Vista para el Texto de la Infobar
    """

    serializer_class = InfoBarSerializer
    queryset = InfoBar.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)
