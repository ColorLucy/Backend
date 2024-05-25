from django.urls import path
from .views import *

urlpatterns = [
    path("create-pedido/", PedidoView.as_view(), name="create_pedido"),
]