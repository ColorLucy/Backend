from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Producto, Detalle, Categoria, Imagen
from rest_framework import serializers


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ImagenSerializer(ModelSerializer):
    class Meta:
        model = Imagen
        fields = ["url"]


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
        fields = ['id_producto', 'nombre', 'fabricante', 'descripcion', 'categoria']


class DetalleProductoSerializer(ModelSerializer):
    producto = ProductoSerializer(many=False)
    imagenes = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Detalle
        fields = ['nombre', 'precio', 'unidad', 'color', 'producto', "imagenes"]


class ProductoDetalleImagenSerializer(serializers.ModelSerializer):
    detalles = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ('id_producto', 'fabricante', 'descripcion', 'categoria', 'detalles')

    def get_detalles(self, obj):
        detalles_queryset = Detalle.objects.filter(producto=obj)
        detalles_data = DetalleSerializer(detalles_queryset, many=True).data

        for detalle in detalles_data:
            imagenes_queryset = Imagen.objects.filter(detalle_id=detalle['id_detalle'])
            imagenes_data = ImagenSerializer(imagenes_queryset, many=True).data
            detalle['imagenes'] = imagenes_data

        return detalles_data

