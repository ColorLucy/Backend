import cloudinary
import cloudinary.uploader
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


class ProductoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductoDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductoSerializer(instance)
        return Response(serializer.data)


class ProductoUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(owner=self.request.user)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductoSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if 'imagen' in request.data:
                imagen = request.data['imagen']
                upload_result = cloudinary.uploader.upload(imagen, folder="here")
                instance.imagen_url = upload_result['secure_url']
                instance.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductoCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  # Asignar el propietario del producto como el usuario autenticado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
