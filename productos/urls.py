from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *
from .views_crud import *

# 1
# # urlpatterns = [
# #     path('productos/', views.ProductoListView.as_view(), name='producto-list'),
# #     path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),
# #     path('productos/<int:pk>/update/', views.ProductoUpdateView.as_view(), name='producto-update'),
# #     path('productos/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto-delete'),
# #     path('productos/create/', views.ProductoCreateView.as_view(), name='producto-create'),
# # ]


urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create-category/", CategoryCreateAPIView.as_view(), name="create_category"),
    path("view-categories/", CategoryListAPIView.as_view(), name="view_categories"),
    path("rud-category/", CategoryDetailAPIView.as_view(), name="rud_category"),

    path("create-product/", ProductCreateAPIView.as_view(), name="create_product"),
    path("view-product/", ProductGetAllAPIView.as_view(), name="view_product"),
    path("view-products/", ProductListAPIView.as_view(), name="view_products"),
    path("update-product/", ProductUpdateAPIView.as_view(), name="update_product"),
    path("delete-product/", ProductDeleteAPIView.as_view(), name="delete_product"),

    path("create-detail/", DetailCreateAPIView.as_view(), name="create_detail"),
    path("view-details/", DetailListAPIView.as_view(), name="view_details"),
    path("rud-detail/", RudDetailAPIView.as_view(), name="rud_detail"),

    
    path("view-details-products/", DetalleProductoApi.as_view(), name="view_details_products"),

    path(
        # Experimental
       "view-image-details/",
        DetailImageListAPIView.as_view(),
        name="view_image_details",
    ),
    path(
        # Experimental
        "view-sliced-details/",
        DetailPaginatedListAPIView.as_view(),
        name="view_sliced_details",
    ),

    path('detalles-por-categoria/<int:categoria_id>/', DetallesPorCategoriaAPIView.as_view(), name='detalles_por_categoria'),


]
