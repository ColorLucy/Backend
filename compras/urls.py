from django.urls import path
from .views import *

urlpatterns = [
    path("orders/", PedidosAPIView.as_view(), name="create_pedido"),
    path("orders/<int:pedido_id>/", PedidoAPIView.as_view(), name="create_pedido"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path('client-order-history/', PedidosClienteView.as_view(), name='client-order-history')
]
