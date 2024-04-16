from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Producto, Detalle, Categoria, Imagen


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["url", "id_imagen"]



class ImagenSerializer(ModelSerializer):
    class Meta:
        model = Imagen
        fields = "__all__"


class DetalleSerializer(ModelSerializer):
    class Meta:
        model = Detalle
        fields = "__all__"


# Experimental Serializer, may be useful in the future or not
class DetalleImagenSerializer(ModelSerializer):
    detalle = DetalleSerializer()

    class Meta:
        model = Imagen
        fields = "__all__"


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto

        fields = '__all__'


class DetalleProductoSerializer(ModelSerializer):
    producto = ProductoSerializer(many=False)
    imagenes = StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Detalle
        fields = ['nombre', 'precio', 'unidad', 'color', 'producto', "imagenes"]

