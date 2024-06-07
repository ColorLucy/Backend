from rest_framework import serializers
from .models import *
from productos.models import *
from productos.serializers import *


class ProductoPedidoReadSerializer(serializers.ModelSerializer):
    detalle = DetalleProductoSerializer(read_only=True)

    class Meta:
        model = ProductoPedido
        fields = ["id_productos_pedido", "detalle", "cantidad"]


class ProductoPedidoWriteSerializer(serializers.ModelSerializer):
    detalle = serializers.PrimaryKeyRelatedField(
        queryset=Detalle.objects.all(), write_only=True
    )

    class Meta:
        model = ProductoPedido
        fields = ["detalle", "cantidad"]


class PedidoPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ["estado"]


class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoPedidoReadSerializer(many=True, read_only=True)
    productos_write = ProductoPedidoWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id_pedido",
            "phone_number",
            "address",
            "tipo_envio",
            "user",
            "fecha_pedido",
            "estado",
            "cantidad_productos",
            "subtotal",
            "total",
            "productos",
            "productos_write",
        ]

    def validate(self, data):
        if not data.get("productos_write"):
            raise serializers.ValidationError(
                "El pedido debe contener al menos un producto."
            )
        return data

    def create(self, validated_data):
        productos_data = validated_data.pop("productos_write")
        pedido = Pedido.objects.create(**validated_data)
        for producto_data in productos_data:
            ProductoPedido.objects.create(pedido=pedido, **producto_data)
        return pedido


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "message", "created_at"]
