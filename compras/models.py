from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.conf import settings
from productos.models import Producto, Detalle, Imagen, Categoria

class Pedido(models.Model):
    ESTADO_PEDIDO_CHOICES = [
        ('recibido', 'Recibido'),
        ('completado', 'Completado'),
    ]

    id_pedido = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    tipo_envio = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PEDIDO_CHOICES, default='recibido')
    cantidad_productos = models.PositiveIntegerField(default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.id_pedido:
            max_id = Pedido.objects.aggregate(max_id=Max("id_pedido"))["max_id"]
            self.id_pedido = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.id_pedido

class ProductoPedido(models.Model):
    id_productos_pedido = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, related_name='productos' , on_delete=models.CASCADE)
    detalle = models.ForeignKey(Detalle, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.id_productos_pedido:
            max_id = ProductoPedido.objects.aggregate(max_id=Max("id_productos_pedido"))["max_id"]
            self.id_productos_pedido = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id_productos_pedido
    
class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
