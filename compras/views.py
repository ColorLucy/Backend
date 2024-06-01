# views.py
import time
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
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
            to=f'whatsapp:{settings.TO_WHATSAPP_NUMBER}'
        )
        return message.sid
    except TwilioRestException as e:
        logger.error(f"Twilio error: {e}")
        return None

def sse_view(request):
    def event_stream():
        last_id = 0
        while True:
            notifications = Notification.objects.filter(id__gt=last_id).order_by('id')
            for notification in notifications:
                yield f'data: {notification.message} {notification.created_at}\n\n'
                last_id = notification.id
            time.sleep(1)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  
    return response

class PedidoView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pedido = serializer.save()

                # Crear mensaje de notificación
                message = f"Se ha creado un nuevo pedido con ID: {pedido.id_pedido} del usuario: {pedido.user}"
                Notification.objects.create(message=message)

                # Enviar notificación por WhatsApp
                body = f'Has recibido un pedido nuevo. Detalles: https://colorlucycali.onrender.com/admin/orders/'
                enviar_notificacion_whatsapp(body)

                # Evento SSE
                sse_view(request)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)