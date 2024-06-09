from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)

class PedidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("Conexión WebSocket iniciada")
        await self.channel_layer.group_add("pedidos", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Conexión WebSocket cerrada: {close_code}")
        await self.channel_layer.group_discard("pedidos", self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Mensaje recibido: {text_data}")
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            "pedidos",
            {
                'type': 'pedido_message',
                'message': message
            }
        )

    async def pedido_message(self, event):
        message = event['message']
        logger.info(f"Enviando mensaje: {message}")
        await self.send(text_data=json.dumps({
            'message': message
        }))