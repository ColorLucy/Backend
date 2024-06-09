from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *
from .views_crud import *

urlpatterns = [
    path("create-category/", CategoryCreateAPIView.as_view(), name="create_category"),
    path("view-categories/", CategoryListAPIView.as_view(), name="view_categories"),
    path("rud-category/", CategoryDetailAPIView.as_view(), name="rud_category"),

    path("create-product/", ProductCreateAPIView.as_view(), name="create_product"),
    path("view-product/", ProductGetAllAPIView.as_view(), name="view_product"),
    path("view-products/", ProductListAPIView.as_view(), name="view_products"),#eliminar esta, no puede estar sin paginacion
    path("update-product/", ProductUpdateAPIView.as_view(), name="update_product"),
    path("delete-product/", ProductDeleteAPIView.as_view(), name="delete_product"),
    path('search/', ProductSearchAPIView.as_view(), name='product-search'),
    path("product-details/", ProductosDetalleAPIView.as_view(), name="view_products_details"),
    path("product-details/<int:producto_id>/", ProductoDetalleAPIView.as_view(), name="view_product_details"),
    path('detalles-por-categoria/<int:categoria_id>/', DetallesPorCategoriaAPIView.as_view(), name='detalles_por_categoria'),

    path('detalles/', DetalleListAPIView.as_view(), name="detalles_list")
]

