from django.urls import path
from .views import *

urlpatterns = [
    path("create-pedido/", PedidoView.as_view(), name="create_pedido"),
    path('sse/', sse_view, name='sse_view'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),

    path('client-order-history', PedidosClienteView.as_view(), name='client-order-history')
]