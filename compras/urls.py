from django.urls import path
from .views import *

urlpatterns = [
    path("orders/", PedidosAPIView.as_view(), name="create_pedido"),
    path("orders/<int:pedido_id>/", PedidoAPIView.as_view(), name="create_pedido"),
    path("sse/", sse_view, name="sse_view"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
]
