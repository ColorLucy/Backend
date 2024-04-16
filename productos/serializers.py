from rest_framework.serializers import ModelSerializer
from .models import Producto, Detalle, Categoria, Imagen


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


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
        fields = "__all__"
