# from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("auth/", include("autenticacion.urls")),
    path("products/", include("productos.urls")),
    path("info/", include("informacion.urls")),
    path("shopping/", include("compras.urls")),
]
