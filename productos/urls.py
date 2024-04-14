from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.ProductoListView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/<int:pk>/update/', views.ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto-delete'),
    path('productos/create/', views.ProductoCreateView.as_view(), name='producto-create'),
]
