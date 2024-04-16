from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

# 1
# # urlpatterns = [
# #     path('productos/', views.ProductoListView.as_view(), name='producto-list'),
# #     path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),
# #     path('productos/<int:pk>/update/', views.ProductoUpdateView.as_view(), name='producto-update'),
# #     path('productos/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto-delete'),
# #     path('productos/create/', views.ProductoCreateView.as_view(), name='producto-create'),
# # ]


urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    path("create-category/", CategoryCreateAPIView.as_view(), name='create_category'),
    path("view-categories/", CategoryListAPIView.as_view(), name="view_categories"),
    path("rud-category/", CategoryDetailAPIView.as_view(), name="rud_category"),

    path("create-product/", ProductCreateAPIView.as_view(), name='create_product'),
    path("view-products/", ProductListAPIView.as_view(), name="view_products"),
    path("rud-product/", ProductDetailAPIView.as_view(), name="rud_product"),  # TODO put

    path("create-detail/", DetailCreateAPIView.as_view(), name="create_detail"),
    path("view-details/", DetailListAPIView.as_view(), name="view_details"),
    path("rud-detail/", RudDetailAPIView.as_view(), name="rud_detail"),

    path("view-details-products/", DetalleProductoApi.as_view(), name="view_details_products"),
]
