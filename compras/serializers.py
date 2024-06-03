# views.py
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
    def get(self, request, *args, **kwargs):
        pedido_id = kwargs.get("pedido_id")
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        serializer = PedidoSerializer(pedido, many=False)
        return Response(serializer.data)


class PedidosAPIView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()

            # Crear mensaje de notificación
            message = f"Se ha creado un nuevo pedido con ID: {pedido.id_pedido} del usuario: {pedido.user}"
            Notification.objects.create(message=message)

            # Enviar notificación por WhatsApp
            body = f"Has recibido un pedido nuevo. Detalles: https://colorlucycali.onrender.com/admin/orders/"
            enviar_notificacion_whatsapp(body)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class PedidosClienteView(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')
        pedidos_cliente = Pedido.objects.filter(user=client_id)
        serializer_pedido = PedidoSerializer(pedidos_cliente, many=True)
        return Response(serializer_pedido.data, status=status.HTTP_200_OK)