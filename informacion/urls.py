from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"infobar", InfoBarView, "infobar")
router.register(r"home/text", HomeTextView, "home-text")
router.register(r"home/start", HomeStartImageView, "home-start")
router.register(r"home/combinations", HomeCombinationsImageView, "home-combinations")
router.register(r"home/products", HomeProductsImageView, "home-products")
router.register(r"home/allies", HomeAlliesImageView, "home-allies")

urlpatterns = [
    path("api/", include(router.urls)),
]
