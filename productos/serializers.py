from django import forms
from rest_framework.serializers import ModelSerializer
from .models import Producto, Detalle, Categoria, Imagen

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ImagenSerializer(ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'


class DetalleSerializer(ModelSerializer):
    #id_imagen1 = ImagenSerializer()
    
    class Meta:
        model = Detalle
        fields = ['nombre', 'precio', 'unidad', 'color', 'producto']


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'