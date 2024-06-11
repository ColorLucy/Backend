from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from twilio.rest import Client
from django.conf import settings
import logging
from twilio.base.exceptions import TwilioRestException
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)


def enviar_notificacion_whatsapp(body):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=settings.TO_WHATSAPP_NUMBER,
        )
        return message.sid
    except TwilioRestException as e:
        logger.error(f"Twilio error: {e}")
        return None


class PedidoAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        pedido_id = kwargs.get("pedido_id")
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        serializer = PedidoSerializer(pedido, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        order_id = kwargs.get("pedido_id")
        order_instance = get_object_or_404(Pedido, pk=order_id)

        new_order_data = request.data
        serializer = PedidoPatchSerializer(
            instance=order_instance, data=new_order_data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Order updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidosAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        pedidos = Pedido.objects.all().order_by("-fecha_pedido")
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()
            # Crear mensaje de notificación
            message = f"Se ha creado un nuevo pedido con ID: {pedido.id_pedido} del usuario: {pedido.user}"
            Notification.objects.create(message=message)
            # Enviar notificación por WhatsApp
            body = f"Has recibido un pedido nuevo. Detalles: https://colorlucycali.onrender.com/admin/order/view/{pedido.id_pedido}"
            enviar_notificacion_whatsapp(body)
            # Enviar notificación al cliente
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pedidos", {"type": "pedido_message", "message": message}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.all().order_by("-created_at")
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class PedidosClienteView(APIView):
    def get(self, request):
        client_id = request.query_params.get("client_id")
        pedidos_cliente = Pedido.objects.filter(user=client_id)
        serializer_pedido = PedidoSerializer(pedidos_cliente, many=True)
        return Response(serializer_pedido.data, status=status.HTTP_200_OK)
