from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path("create/", ProductCreateAPIView.as_view(), name="create_product"),
    path("list/", ProductListAPIView.as_view(), name="list_products"),
    path("detail/", ProductDetailAPIView.as_view(), name="edit_products"),
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    path("create-category/", CategoryCreateAPIView.as_view(), name='create_category'),
    path("create-product/", ProductCreateAPIView.as_view(), name='create_product'),
    #path("create-detail/", DetailCreateAPIView.as_view(), name='create_detail'),

]