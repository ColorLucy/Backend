from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    path("create-category/", CategoryCreateAPIView.as_view(), name='create_category'),
    path("view-categories/", CategoryListAPIView.as_view(), name="view_categories"),
    path("rud-category/", CategoryDetailAPIView.as_view(), name="rud_category"), #TODO put

    path("create-product/", ProductCreateAPIView.as_view(), name='create_product'),
    path("view-products/", ProductListAPIView.as_view(), name="view_products"),
    path("rud-product/", ProductDetailAPIView.as_view(), name="rud_product"), #TODO put

    path("create-detail/", DetailCreateAPIView.as_view(), name="create_detail"),
    path("view-details/", DetailListAPIView.as_view(), name="view_details"),
    path("rud-detail/", RudDetailAPIView.as_view(), name="rud_detail") #TODO put
    
    
]