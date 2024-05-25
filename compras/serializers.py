from rest_framework import serializers
from .models import *
from productos.models import *
from productos.serializers import *

class ProductoSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer(many=True, read_only=True)
    imagenes = ImagenSerializer(many=True, read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

class ProductoPedidoSerializer(serializers.ModelSerializer):
    # producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), write_only=True)
    detalle = serializers.PrimaryKeyRelatedField(queryset=Detalle.objects.all(), write_only=True)
    # categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), write_only=True)
    # imagenes = serializers.PrimaryKeyRelatedField(queryset=Imagen.objects.all(), write_only=True, required=False, allow_null=True)

    class Meta:
        model = ProductoPedido
        fields =[ 'id_productos_pedido', 'detalle', 'cantidad']
        # fields = ['id_productos_pedido', 'producto', 'detalle', 'categoria', 'imagenes', 'cantidad']

class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'phone_number', 'address', 'tipo_envio', 'user', 'fecha_pedido', 'estado', 'cantidad_productos','subtotal', 'total', 'productos']

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        pedido = Pedido.objects.create(**validated_data)
        for producto_data in productos_data:
            ProductoPedido.objects.create(pedido=pedido, **producto_data)
        return pedido